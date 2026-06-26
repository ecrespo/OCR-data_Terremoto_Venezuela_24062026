"""
App web de búsqueda semántica de pacientes (Flask + sqlite-vec).

Uso:
    python ingest.py        # una vez, para crear ../consolidado_vec.db
    python app.py           # abre http://127.0.0.1:5000
"""
from __future__ import annotations
import os

from flask import Flask, request, jsonify, render_template_string

import search as S

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.environ.get("VEC_DB", os.path.normpath(os.path.join(HERE, "..", "consolidado_vec.db")))

app = Flask(__name__)

PAGE = """<!doctype html><html lang=es><head><meta charset=utf-8>
<meta name=viewport content="width=device-width, initial-scale=1">
<title>Búsqueda de pacientes — Sismo Venezuela 2026</title>
<style>
:root{--bg:#0f1720;--card:#172230;--ink:#e7eef6;--mut:#90a4b8;--acc:#3b82f6;--line:#26384b}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font-family:system-ui,Segoe UI,Arial,sans-serif;line-height:1.45}
.wrap{max-width:1000px;margin:0 auto;padding:24px}
h1{font-size:20px;margin:0 0 4px}.sub{color:var(--mut);font-size:13px;margin-bottom:18px}
form{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:8px}
input,select{background:var(--card);border:1px solid var(--line);color:var(--ink);
padding:10px 12px;border-radius:8px;font-size:14px}
input[type=text]{flex:1;min-width:240px}
button{background:var(--acc);border:0;color:#fff;padding:10px 18px;border-radius:8px;
font-size:14px;cursor:pointer}
.meta{color:var(--mut);font-size:12px;margin:6px 0 14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;
padding:12px 14px;margin-bottom:10px}
.card h3{margin:0 0 4px;font-size:15px}
.badge{display:inline-block;background:#0d2440;color:#7db4ff;border:1px solid #1d4e86;
padding:1px 8px;border-radius:999px;font-size:11px;margin-left:6px}
.row2{color:var(--mut);font-size:13px}
.note{color:#d6b25e;font-size:12px;margin-top:4px}
.dist{float:right;color:var(--mut);font-size:12px}
.empty{color:var(--mut);padding:20px 0}
.tips{color:var(--mut);font-size:12px;margin-top:18px}
.tips a{color:#7db4ff;cursor:pointer;text-decoration:underline}
</style></head><body><div class=wrap>
<h1>Búsqueda semántica de pacientes</h1>
<div class=sub>Terremoto Venezuela · 24/06/2026 — consolidado de hospitales</div>
<form onsubmit="go(event)">
  <input id=q type=text placeholder="Ej.: niño rescatado en La Guaira con fractura"
         value="{{q}}" autofocus>
  <select id=hospital>
    <option value="">Todos los hospitales</option>
    {% for h in hospitales %}<option value="{{h}}">{{h}}</option>{% endfor %}
  </select>
  <select id=k>
    <option>10</option><option>20</option><option>30</option>
  </select>
  <button>Buscar</button>
</form>
<div class=meta>BD: <b>{{meta.get('embedder','?')}}</b> · dim {{meta.get('dim','?')}}
 · {{meta.get('registros','?')}} pacientes · creada {{meta.get('fecha','?')}}</div>
<div id=out><div class=empty>Escribe una consulta para empezar.</div></div>
<div class=tips>Ideas:
 <a onclick="ej('fractura de fémur')">fractura de fémur</a> ·
 <a onclick="ej('niños solos sin familiar')">niños solos sin familiar</a> ·
 <a onclick="ej('persona fallecida')">persona fallecida</a> ·
 <a onclick="ej('rescatado bajo escombros en Caraballeda')">rescatado en Caraballeda</a>
</div>
</div>
<script>
async function go(e){e&&e.preventDefault();
 const q=document.getElementById('q').value.trim();if(!q)return;
 const k=document.getElementById('k').value, h=document.getElementById('hospital').value;
 const out=document.getElementById('out');out.innerHTML='<div class=empty>Buscando…</div>';
 const r=await fetch('/api/search?q='+encodeURIComponent(q)+'&k='+k+'&hospital='+encodeURIComponent(h));
 const d=await r.json();
 if(!d.results.length){out.innerHTML='<div class=empty>Sin resultados.</div>';return;}
 out.innerHTML=d.results.map(x=>`<div class=card>
   <span class=dist>similitud ${x.score}</span>
   <h3>${esc(x.nombre)} <span class=badge>${esc(x.edad||'s/e')}</span></h3>
   <div class=row2>${esc(x.hospital)}</div>
   <div class=row2>${[x.cedula,x.procedencia,x.servicio].filter(Boolean).map(esc).join(' · ')}</div>
   ${x.nota?`<div class=note>${esc(x.nota)}</div>`:''}
 </div>`).join('');
}
function ej(t){document.getElementById('q').value=t;go();}
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
</script></body></html>"""


def get_con():
    return S.connect(DB)


@app.route("/")
def home():
    con = get_con()
    meta = S.db_meta(con)
    hosp = [r[0] for r in con.execute(
        "SELECT DISTINCT hospital FROM pacientes ORDER BY hospital")]
    con.close()
    return render_template_string(PAGE, q="", meta=meta, hospitales=hosp)


@app.route("/api/search")
def api_search():
    q = request.args.get("q", "").strip()
    k = int(request.args.get("k", 10))
    hospital = request.args.get("hospital") or None
    con = get_con()
    rows = S.search(con, q, k=k, hospital=hospital) if q else []
    con.close()
    res = []
    for r in rows:
        # distancia coseno -> similitud aproximada 0..1
        score = round(max(0.0, 1 - r["distance"] / 2), 3)
        res.append(dict(nombre=r["nombre"], edad=r["edad"], hospital=r["hospital"],
                        cedula=r["cedula"], procedencia=r["procedencia"],
                        servicio=r["servicio"], nota=r["nota"], score=score))
    return jsonify(results=res)


if __name__ == "__main__":
    if not os.path.exists(DB):
        raise SystemExit(f"No existe {DB}. Ejecuta primero: python ingest.py")
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)
