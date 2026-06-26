# OCR — Terremoto Venezuela (24/06/2026)

Transcripción de listas manuscritas de pacientes atendidos en hospitales tras el terremoto del 24 de junio de 2026.

> Las cédulas se transcribieron tal como se leen; algunas pueden tener errores de lectura por la caligrafía. Las celdas marcadas con `—` no tenían dato legible en la imagen.

## ⚙️ Entorno (uv)

El repositorio usa **[uv](https://docs.astral.sh/uv/)** como gestor de paquetes
(`pyproject.toml` + `uv.lock`). Para preparar el entorno:

```bash
uv sync                 # instala dependencias
```

Salidas de datos: `consolidado.md`, `consolidado.xlsx`, `consolidado.csv`,
`consolidado.db` (SQLite) y `consolidado_vec.db` (SQLite + sqlite-vec).
La app de **búsqueda semántica** está en [`consolidado_app/`](consolidado_app/README.md):

```bash
uv run python consolidado_app/ingest.py     # genera la base vectorial
uv run python consolidado_app/app.py        # interfaz web de búsqueda
```

## 📋 Documento principal — Lista consolidada

➡️ **[Lista de heridos consolidada por hospitales](data/20260626/Lista_GCal_Consolidada/Lista_heridos_consolidada.md)**

Listado unificado de heridos de todos los hospitales en un solo documento. Es el punto de entrada principal mientras se completa el procesamiento día por día (ver el índice por fecha más abajo).

## Índice por fecha y hospital

### 2026-06-26

| Hospital / Centro | Listas | Documento |
|-------------------|--------|-----------|
| Hospital General Regional Dr. José María Vargas (IVSS, La Guaira) | Lista de pacientes atendidos (172 pacientes — 8 listas de 20 + continuación de 12) | [Hosp_Jose_Maria_Vargas.md](data/20260626/Hosp_General_DR_Jose_Maria_Vargas_La_Guaira/Hosp_Jose_Maria_Vargas.md) |
| Consolidado por hospitales | Lista de heridos consolidada (primeras 100 filas de la hoja de Google Sheets) | [Lista_heridos_consolidada.md](data/20260626/Lista_GCal_Consolidada/Lista_heridos_consolidada.md) |

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