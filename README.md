# Kuis Trivia API

A FastAPI project that serves Indonesian-language trivia questions from a bundled JSON file. It supports category filtering, a question count limit, and an interactive OpenAPI reference.

## Run Locally

From the repository root, create a Python 3.12 virtual environment:

```bash
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on macOS or Linux, or `\.venv\Scripts\Activate.ps1` in Windows PowerShell. Then install the dependencies and start the API:

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open [interactive API docs](http://127.0.0.1:8000/docs) while the local server is running. The hosted endpoint from the original deployment currently returns an error, so the examples below use the local server.

## Browse Categories and Questions

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/kategori/
curl "http://127.0.0.1:8000/soal/?kategori=sejarah&jumlah=3"
```

Omit `kategori` to list questions across categories. Set `jumlah` to a number from 1 to 50. The bundled categories are `geografi`, `sains`, `sejarah`, and `umum`.

## Repository Contents

- [main.py](main.py) — FastAPI application and health response.
- [app/routers/](app/routers/) — Category and question routes.
- [app/data/soal_data.json](app/data/soal_data.json) — Bundled trivia questions.
- [requirements.txt](requirements.txt) — Python dependencies.
- [Dockerfile](Dockerfile) — Container build for the API.
- [CLOUD_BUILD_SETUP.md](CLOUD_BUILD_SETUP.md) — Deployment notes from the original project.

The project includes an [MIT license](LICENSE).
