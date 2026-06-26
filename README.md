# OCR — Terremoto Venezuela (24/06/2026)

Transcripción de listas manuscritas de pacientes atendidos en hospitales tras el terremoto del 24 de junio de 2026.

> Las cédulas se transcribieron tal como se leen; algunas pueden tener errores de lectura por la caligrafía. Las celdas marcadas con `—` no tenían dato legible en la imagen.

## ⚙️ Entorno (uv)

El repositorio usa **[uv](https://docs.astral.sh/uv/)** como gestor de paquetes
(`pyproject.toml` + `uv.lock`). Para preparar el entorno:

```bash
uv sync                 # instala dependencias
```

## 📋 Documento principal — Lista consolidada

➡️ **[consolidado.md](consolidado.md)** — listado unificado y **deduplicado** de todas las listas (**1.117 personas** en 12 centros asistenciales), con una columna *Hospital / Área*, un resumen por centro y notas de consolidación.

## 🔎 Archivos consolidados (salidas)

El mismo conjunto de datos en varios formatos (todos se generan a partir de las listas de `data/`):

| Archivo | Formato | Uso |
|---------|---------|-----|
| [consolidado.md](consolidado.md) | Markdown | Tabla legible con columna *Hospital / Área*, resumen y notas. |
| [consolidado.csv](consolidado.csv) | CSV (UTF-8 con BOM) | Importable directo en Excel / Google Sheets / pandas. |
| [consolidado.xlsx](consolidado.xlsx) | Excel | Hoja *Resumen* (con fórmulas) + hoja *Consolidado* con filtros; filas nuevas del registro UCV resaltadas. |
| [consolidado.db](consolidado.db) | SQLite | Tabla `pacientes` + vista `resumen_hospital`. Ej.: `SELECT * FROM pacientes WHERE cedula='15720959';` |
| [consolidado_vec.db](consolidado_vec.db) | SQLite + sqlite-vec | Base **vectorial** para búsqueda semántica (la consume la app). |

> Para regenerar todo tras cambiar las listas: actualizar `consolidado.md` y reconstruir CSV/XLSX/DB; la base vectorial se rehace con `uv run python consolidado_app/ingest.py`.

## 🤖 App de búsqueda semántica — [`consolidado_app/`](consolidado_app/README.md)

Búsqueda por similitud (**sqlite-vec**) sobre los pacientes, con CLI e interfaz web. Backends de embeddings: *fastembed* (semántico, local, por defecto) · *OpenAI* (opcional) · *hashing* (respaldo offline). Detalles en [consolidado_app/README.md](consolidado_app/README.md).

```bash
uv sync                                                       # instala dependencias
uv run python consolidado_app/ingest.py                       # genera consolidado_vec.db (embeddings)
uv run python consolidado_app/search.py "fractura de fémur" --hospital Vargas   # búsqueda por consola
uv run python consolidado_app/app.py                          # interfaz web: http://127.0.0.1:5000
```

## Índice por fecha y hospital

### 2026-06-26

| Hospital / Centro | Listas | Documento |
|-------------------|--------|-----------|
| Hospital General Regional Dr. José María Vargas (IVSS, La Guaira) | Lista de pacientes atendidos (172 pacientes — 8 listas de 20 + continuación de 12) | [Hosp_Jose_Maria_Vargas.md](data/20260626/Hosp_General_DR_Jose_Maria_Vargas_La_Guaira/Hosp_Jose_Maria_Vargas.md) |
| Consolidado por hospitales | Lista de heridos consolidada (primeras 100 filas de la hoja de Google Sheets) | [Lista_heridos_consolidada.md](data/20260626/Lista_GCal_Consolidada/Lista_heridos_consolidada.md) |
| Registro Maestro oficial (11 centros) | Consolidado UCV — pacientes por hospital (906 registros, corte 25JUN26 19:00) | [Consolidado_UCV.md](data/20260626/Consolidado_UCV/Consolidado_UCV.md) |
| Cruz Roja Venezolana (sede La Candelaria, Caracas) | Lista de personas atendidas (31 personas) | [Cruz_Roja_Candelaria.md](data/20260626/Cruz_Roja/Cruz_Roja_Candelaria.md) |
| Google Drive «SISMO 2026 VZLA» (varios centros + campo de golf) | Extracción de DOCX/PDF/fotos: consolidado, registro maestro, HUC, Vargas, Luciani, Pérez Carreño, sobrevivientes campo de golf | [SISMO_2026_VZLA/](data/20260626/SISMO_2026_VZLA/README.md) |

### 2026-06-25

| Hospital / Centro | Listas | Documento |
|-------------------|--------|-----------|
| Hospital Miguel Pérez Carreño | Lista 1–4, Triaje, Traumashock | [Hosp_Perez_Carreño.md](data/20260625/Hosp_Perez_Carreño/Hosp_Perez_Carreño.md) |
| Hospital Miguel Pérez Carreño | Pediatría — niños (1–17) | [Lista_Niños_Hosp_Perez_Carreño.md](data/20260625/Hosp_Perez_Carreño/Lista_Niños_Hosp_Perez_Carreño.md) |
| Hospital Miguel Pérez Carreño (La Yaguara) | Heridos trasladados desde La Guaira (82 registros, 5 nuevos) | [Hosp_Perez_Carreño_La_Yaguara.md](data/20260625/Hosp_Perez_Carreño/Hosp_Perez_Carreño_La_Yaguara.md) |
| Hospital Miguel Pérez Carreño | Pediatría — procedencia, registros nuevos (1–14) | [lista2.md](data/20260625/Hosp_Perez_Carreño/lista2.md) |
| Alcaldía de Chacao (Los Palos Grandes / Bellocampo) | Reporte de rescatados (17 rescatados, 12 fallecidos) | [reporte_rescatados_chacao.md](data/20260625/Alcaldia_Chacao/reporte_rescatados_chacao.md) |
| Periférico de Catia (heridos de La Guaira) | Registro de emergencia (correlativos 679–740) | [PersonasRescatadas.md](data/20260625/LaGuaira/PersonasRescatadas.md) |
| Hospital Dr. Domingo Luciani (Llanito) | Pacientes ingresados por sismo (1–37) | [PersonasHeridas.md](data/20260625/Hosp_Domingo_Luciani/PersonasHeridas.md) |
| Hospital Dr. Domingo Luciani (Llanito) | Niños solos en Cirugía Pediátrica (1–5) | [CirugiaPediatrica.md](data/20260625/Hosp_Domingo_Luciani/CirugiaPediatrica.md) |
| Hospital Dr. Domingo Luciani (Llanito) | Registros nuevos no repetidos + triaje de cirugía | [Listado_Domingo_Luciani.md](data/20260625/Hosp_Domingo_Luciani/Listado_Domingo_Luciani.md) |