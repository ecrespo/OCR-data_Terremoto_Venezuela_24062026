"""
Ingesta: lee consolidado.csv, genera embeddings y los guarda en una BD SQLite
con la extensión sqlite-vec (tabla virtual vec0) para búsqueda por similitud.

Uso:
    python ingest.py                      # usa consolidado.csv y crea consolidado_vec.db
    python ingest.py --embedder hashing   # fuerza un backend concreto
    python ingest.py --csv ../consolidado.csv --db ../consolidado_vec.db

Estructura de la BD resultante:
    pacientes(rowid, hospital, nombre, edad, cedula, procedencia, servicio, nota, texto)
    vec_pacientes  -> vec0(embedding float[DIM])   (rowid = pacientes.rowid)
    meta(clave, valor)  -> embedder, dim, modelo, fecha
"""
from __future__ import annotations
import argparse
import csv
import datetime as dt
import os
import sqlite3
import struct

import sqlite_vec

from embedders import get_embedder

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = os.path.normpath(os.path.join(HERE, "..", "consolidado.csv"))
DEFAULT_DB = os.path.normpath(os.path.join(HERE, "..", "consolidado_vec.db"))


def row_text(r: dict) -> str:
    """Texto que se vectoriza por paciente (lo más informativo posible)."""
    parts = [r.get("Nombre", ""), r.get("Hospital / Área", ""),
             r.get("Procedencia / Zona", ""), r.get("Servicio / Lista", ""),
             r.get("Edad", ""), r.get("Nota", "")]
    return " · ".join(p for p in parts if p)


def serialize(vec) -> bytes:
    return struct.pack(f"{len(vec)}f", *vec)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=DEFAULT_CSV)
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--embedder", default=None,
                    help="fastembed | openai | hashing (por defecto: auto)")
    ap.add_argument("--batch", type=int, default=64)
    args = ap.parse_args()

    with open(args.csv, encoding="utf-8-sig") as f:
        rows = [r for r in csv.DictReader(f)]
    print(f"Leídos {len(rows)} registros de {args.csv}")

    emb = get_embedder(args.embedder)
    print(f"Embedder: {emb.name} (dim={emb.dim})")

    if os.path.exists(args.db):
        os.remove(args.db)
    con = sqlite3.connect(args.db)
    con.enable_load_extension(True)
    sqlite_vec.load(con)
    con.enable_load_extension(False)
    cur = con.cursor()

    cur.execute("""CREATE TABLE pacientes(
        rowid INTEGER PRIMARY KEY,
        hospital TEXT, nombre TEXT, edad TEXT, cedula TEXT,
        procedencia TEXT, servicio TEXT, nota TEXT, texto TEXT)""")
    cur.execute("CREATE INDEX idx_cedula ON pacientes(cedula)")
    cur.execute("CREATE INDEX idx_hospital ON pacientes(hospital)")
    cur.execute(f"CREATE VIRTUAL TABLE vec_pacientes USING vec0(embedding float[{emb.dim}])")
    cur.execute("CREATE TABLE meta(clave TEXT PRIMARY KEY, valor TEXT)")

    texts = [row_text(r) for r in rows]
    for i, r in enumerate(rows, 1):
        cur.execute(
            "INSERT INTO pacientes VALUES(?,?,?,?,?,?,?,?,?)",
            (i, r.get("Hospital / Área", ""), r.get("Nombre", ""), r.get("Edad", ""),
             r.get("Cédula", ""), r.get("Procedencia / Zona", ""),
             r.get("Servicio / Lista", ""), r.get("Nota", ""), texts[i - 1]))

    n = 0
    for s in range(0, len(texts), args.batch):
        chunk = texts[s:s + args.batch]
        vecs = emb.embed(chunk)
        for j, v in enumerate(vecs):
            cur.execute("INSERT INTO vec_pacientes(rowid, embedding) VALUES (?, ?)",
                        (s + j + 1, serialize(v)))
        n += len(chunk)
        print(f"  embeddings {n}/{len(texts)}", end="\r")
    print()

    for k, v in {"embedder": emb.name, "dim": str(emb.dim),
                 "registros": str(len(rows)),
                 "fecha": dt.datetime.now().isoformat(timespec="seconds")}.items():
        cur.execute("INSERT OR REPLACE INTO meta VALUES(?,?)", (k, v))

    con.commit()
    con.close()
    print(f"OK -> {args.db}  ({len(rows)} pacientes, embedder={emb.name})")


if __name__ == "__main__":
    main()
