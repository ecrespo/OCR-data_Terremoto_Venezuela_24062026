"""
Búsqueda semántica por línea de comandos sobre la BD vectorial.

Uso:
    python search.py "niño con fractura rescatado en La Guaira"
    python search.py "fractura de femur" -k 10 --hospital Vargas
"""
from __future__ import annotations
import argparse
import os
import sqlite3
import struct

import sqlite_vec

from embedders import get_embedder

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DB = os.path.normpath(os.path.join(HERE, "..", "consolidado_vec.db"))


def connect(db_path):
    con = sqlite3.connect(db_path)
    con.enable_load_extension(True)
    sqlite_vec.load(con)
    con.enable_load_extension(False)
    con.row_factory = sqlite3.Row
    return con


def db_meta(con):
    return {r["clave"]: r["valor"] for r in con.execute("SELECT clave, valor FROM meta")}


def search(con, query, k=10, hospital=None, embedder_name=None):
    meta = db_meta(con)
    emb = get_embedder(embedder_name or _embedder_kind(meta.get("embedder", "")))
    if emb.name != meta.get("embedder"):
        print(f"[aviso] la BD se creó con '{meta.get('embedder')}' y se está consultando "
              f"con '{emb.name}'. Para mejores resultados regenera con: python ingest.py")
    qv = struct.pack(f"{emb.dim}f", *emb.embed([query])[0])
    # KNN amplio y luego filtro opcional por hospital
    rows = con.execute("""
        SELECT p.rowid, p.hospital, p.nombre, p.edad, p.cedula, p.procedencia,
               p.servicio, p.nota, v.distance
        FROM vec_pacientes v JOIN pacientes p ON p.rowid = v.rowid
        WHERE v.embedding MATCH ? AND k = ?
        ORDER BY v.distance
    """, (qv, max(k * 5, 50))).fetchall()
    if hospital:
        h = hospital.lower()
        rows = [r for r in rows if h in (r["hospital"] or "").lower()]
    return rows[:k]


def _embedder_kind(name):
    if name.startswith("fastembed"):
        return "fastembed"
    if name.startswith("openai"):
        return "openai"
    return "hashing"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("query")
    ap.add_argument("-k", type=int, default=10)
    ap.add_argument("--hospital", default=None)
    ap.add_argument("--db", default=DEFAULT_DB)
    args = ap.parse_args()

    con = connect(args.db)
    rows = search(con, args.query, args.k, args.hospital)
    print(f'\nResultados para: "{args.query}"\n' + "-" * 70)
    for i, r in enumerate(rows, 1):
        print(f"{i:2d}. [{r['distance']:.3f}] {r['nombre']}  ({r['edad'] or 's/e'})"
              f"  · {r['hospital']}")
        extra = " / ".join(x for x in (r["cedula"], r["procedencia"], r["servicio"]) if x)
        if extra:
            print(f"      {extra}")
        if r["nota"]:
            print(f"      nota: {r['nota']}")
    print()


if __name__ == "__main__":
    main()
