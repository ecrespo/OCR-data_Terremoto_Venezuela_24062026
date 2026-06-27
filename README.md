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

### 2026-06-27

| Hospital / Centro | Listas | Documento |
|-------------------|--------|-----------|
| Hospital Dr. Domingo Luciani (Llanito) | Lista actualizada de últimos ingresos por servicio (27/06, 9:00 am — 40 pacientes) | [Hosp_Domingo_Luciani_27JUN.md](data/20260627/Hosp_Domingo_Luciani_191300/Hosp_Domingo_Luciani_27JUN.md) |

### 2026-06-26

| Hospital / Centro | Listas | Documento |
|-------------------|--------|-----------|
| Hospital General Regional Dr. José María Vargas (IVSS, La Guaira) | Lista de pacientes atendidos (172 pacientes — 8 listas de 20 + continuación de 12) | [Hosp_Jose_Maria_Vargas.md](data/20260626/Hosp_General_DR_Jose_Maria_Vargas_La_Guaira/Hosp_Jose_Maria_Vargas.md) |
| Consolidado por hospitales | Lista de heridos consolidada (primeras 100 filas de la hoja de Google Sheets) | [Lista_heridos_consolidada.md](data/20260626/Lista_GCal_Consolidada/Lista_heridos_consolidada.md) |
| Registro Maestro oficial (11 centros) | Consolidado UCV — pacientes por hospital (906 registros, corte 25JUN26 19:00) | [Consolidado_UCV.md](data/20260626/Consolidado_UCV/Consolidado_UCV.md) |
| Cruz Roja Venezolana (sede La Candelaria, Caracas) | Lista de personas atendidas (31 personas) | [Cruz_Roja_Candelaria.md](data/20260626/Cruz_Roja/Cruz_Roja_Candelaria.md) |
| Google Drive «SISMO 2026 VZLA» (varios centros + campo de golf) | Extracción de DOCX/PDF/fotos: consolidado, registro maestro, HUC, Vargas, Luciani, Pérez Carreño, sobrevivientes campo de golf | [SISMO_2026_VZLA/](data/20260626/SISMO_2026_VZLA/README.md) |
| Registro Maestro oficial (14 centros) | Consolidado «dropbox» — pacientes por hospital (2.257 registros, corte 26JUN26 10:41) | [consolidado_dropbox.md](data/20260626/consolidado_dropbox/consolidado_dropbox.md) |
| Registro Maestro oficial (16 centros) | Consolidado por hospital (2.743 registros, corte 26JUN26 15:12; incluye Ricardo Baquero González y Centro de Acopio Caraballeda) | [consolidado_26JUN26_1512.md](data/20260626/Consolidado_26JUN26_1512/consolidado_26JUN26_1512.md) |
| Google Drive «SISMO 2026 VZLA» (carga 15:54) | Material nuevo: Periférico de Catia / Ricardo Baquero González (camas + cédulas), Pérez Carreño Trauma Shock (26/06, 1 fallecido), fotos Luciani 26/06 | [SISMO_2026_VZLA_1554/](data/20260626/SISMO_2026_VZLA_1554/README.md) |
| Infografía «337 personas en riesgo» (5 centros) | Listado de personas en riesgo agrupado por hospital (319 de 337 transcritas; faltan N° 259–267 y 286–294 por legibilidad) | [Listado_337_personas_en_riesgo.md](data/20260626/Listado_337_Personas_en_Riesgo/Listado_337_personas_en_riesgo.md) |
| Google Drive «SISMO 2026 VZLA» (carga 18:04) | Pérez Carreño: Listado de pacientes en **Piso 1** (73, con cédula) y **Pediatría** 26/06 (20) | [data1804/](data/20260626/data1804/README.md) |
| Google Sheets «lista_heridos_hospitales_consolidada» (11 hojas) | Extracción por hospital de la hoja de Google (392 personas en 8 centros, incl. Materno Infantil del Valle y dos listas «Sin identificar») | [1949/](data/20260626/1949/README.md) |
| Google Sheets «VENEZUELA HOSPITALES - TERREMOTO» (4 hojas) | Registro detallado por hospital (2.248 personas en 17 centros, con cédula/dirección/lesión/diagnóstico) + No encontrados, Residencias y Sobrevivientes | [203000/](data/20260626/203000/README.md) |
| Hospital Dr. Domingo Luciani (Llanito) | Heridos por servicio (listas de pared del 26/06 — 120 pacientes) | [Hosp_Domingo_Luciani_26JUN26.md](data/20260626/Hosp_Domingo_Luciani/Hosp_Domingo_Luciani_26JUN26.md) |
| Hospital Miguel Pérez Carreño | Pacientes por sismo del 26/06 (219 personas + 17 emergencia pediátrica) | [Hosp_Perez_Carreno_26JUN.md](data/20260626/Hosp_Perez_Carreno_1440/Hosp_Perez_Carreno_26JUN.md) |
| Centro de Acopio de La Guaira (Campo de Golf) | Personas en el centro de acopio (292 personas) | [Centro_Acopio_La_Guaira_Campo_Golf.md](data/20260626/Centro_Acopio_La_Guaira_Campo_Golf/Centro_Acopio_La_Guaira_Campo_Golf.md) |

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