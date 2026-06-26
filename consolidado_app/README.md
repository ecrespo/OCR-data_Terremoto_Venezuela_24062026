# Búsqueda semántica de pacientes — sqlite-vec

App de búsqueda por similitud sobre el consolidado de pacientes del terremoto
(Venezuela, 24/06/2026). Usa **[sqlite-vec](https://github.com/asg017/sqlite-vec)**
para almacenar embeddings dentro de un único archivo SQLite y hacer búsqueda
*k-NN*, con una interfaz web y una CLI.

```
consolidado_app/
├── embedders.py     # backends de embeddings (fastembed / OpenAI / fallback offline)
├── ingest.py        # lee ../consolidado.csv y crea ../consolidado_vec.db
├── search.py        # búsqueda por línea de comandos
├── app.py           # interfaz web (Flask)
└── requirements.txt
```

La BD vectorial se genera en la raíz del repo: `../consolidado_vec.db`.

## Instalación (con uv)

El repo usa **[uv](https://docs.astral.sh/uv/)** como gestor de paquetes
(`pyproject.toml` + `uv.lock` en la raíz). Desde la **raíz del repositorio**:

```bash
uv sync                    # crea el entorno con todas las dependencias
uv sync --extra openai     # (opcional) añade el backend de OpenAI
```

> Alternativa con pip: `pip install -r consolidado_app/requirements.txt`

## Uso

Todos los comandos se ejecutan desde la **raíz del repo** con `uv run`:

```bash
# 1) Generar la base vectorial desde consolidado.csv (una sola vez)
uv run python consolidado_app/ingest.py

# 2a) Buscar por consola
uv run python consolidado_app/search.py "niño rescatado en La Guaira con fractura" -k 10
uv run python consolidado_app/search.py "fractura de fémur" --hospital Vargas

# 2b) o abrir la interfaz web
uv run python consolidado_app/app.py        # http://127.0.0.1:5000
```

## Embeddings (backends)

`ingest.py` elige automáticamente el mejor disponible; se puede forzar con
`--embedder`:

| Backend | Cómo se activa | Notas |
|---|---|---|
| **fastembed** *(recomendado)* | viene en `requirements.txt` | Modelo multilingüe local `paraphrase-multilingual-MiniLM-L12-v2` (ONNX, **sin API key**). Descarga ~470 MB la primera vez. Búsqueda **semántica** real. |
| **openai** | `pip install openai` + `OPENAI_API_KEY` | `text-embedding-3-small`. Envía texto a la API (ojo con datos sensibles). |
| **hashing** | siempre disponible | Fallback **offline** sin dependencias ni red. Es léxico/fuzzy (no semántico); útil para nombres con errores de OCR y para que la app funcione sin descargar nada. |

> La BD guarda con qué backend y dimensión se creó (tabla `meta`). Si consultas
> con un backend distinto al de la ingesta, la app avisa: regenera con
> `python ingest.py` para que coincidan.

### Nota sobre la BD incluida

El archivo `consolidado_vec.db` que viene en el repo se generó con el backend
**hashing** (offline). Para activar la **búsqueda semántica** ejecuta una vez
(desde la raíz del repo):

```bash
uv sync
uv run python consolidado_app/ingest.py   # reconstruye con fastembed (multilingüe)
```

## Cómo funciona

1. Por cada paciente de `consolidado.csv` se arma un texto
   (`nombre · hospital · procedencia · servicio · edad · nota`).
2. Se vectoriza y se inserta en una tabla virtual `vec0(embedding float[DIM])`.
3. La consulta se vectoriza con el mismo modelo y se buscan los vecinos más
   cercanos (`embedding MATCH ? AND k = ?`), con filtro opcional por hospital.

## Regenerar tras actualizar los datos

Si cambia `consolidado.csv`, vuelve a ejecutar `uv run python consolidado_app/ingest.py`.
