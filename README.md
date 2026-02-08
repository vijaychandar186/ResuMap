# ResuMap

Resume extraction API powered by [NuExtract](https://huggingface.co/numind/NuExtract-tiny-v1.5). Upload a PDF or DOCX resume and get back structured JSON with contact info, skills, experience, and education.

Built with FastAPI and llama-cpp-python. Uses a sliding window approach to handle long documents within the model's 8192-token context window.

## Project Structure

```
app/
  main.py              # FastAPI app, lifespan, CORS
  config.py            # Settings (env vars with RESUMAP_ prefix)
  models.py            # Pydantic response schemas
  dependencies.py      # LLM dependency injection
  routers/
    extract.py         # POST /extract endpoint
  services/
    llm.py             # Model loading, tokenization, inference
    sliding_window.py  # Token-based document chunking
    file_parser.py     # PDF and DOCX text extraction
    extraction.py      # Extraction orchestration
  core/
    templates.py       # Resume JSON template
scripts/
  download_model.py    # One-time model download
```

## Setup

### Option 1: pip

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Download the model (one-time)
python -m scripts.download_model

# Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Option 2: uv

```bash
uv sync

# Download the model (one-time)
uv run python -m scripts.download_model

# Start the server
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Option 3: Docker

```bash
docker build -t resumap .
docker run -p 8000:8000 resumap
```

### Option 4: Docker Compose

```bash
docker compose up --build
```

The Docker image downloads the model at build time, so no extra setup is needed.

## Usage

```bash
# Extract from a PDF
curl -X POST http://localhost:8000/extract -F "file=@resume.pdf"

# Extract from a DOCX
curl -X POST http://localhost:8000/extract -F "file=@resume.docx"
```

### Response

```json
{
  "success": true,
  "data": {
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "phone": "+1 415 555 0198",
    "location": "San Francisco, CA",
    "skills": ["Python", "FastAPI", "Docker"],
    "experience": [
      {
        "company": "Stripe",
        "title": "Senior Backend Engineer",
        "start_date": "Jan 2021",
        "end_date": "Present",
        "location": "San Francisco, CA"
      }
    ],
    "education": [
      {
        "degree": "B.S. in Computer Science",
        "institution": "University of Washington",
        "year": "2018"
      }
    ]
  },
  "chunks_processed": 1
}
```

## Configuration

All settings can be overridden via environment variables with the `RESUMAP_` prefix:

| Variable | Default | Description |
|---|---|---|
| `RESUMAP_MODEL_N_CTX` | `8192` | Model context window size |
| `RESUMAP_MODEL_N_THREADS` | `8` | CPU threads for inference |
| `RESUMAP_MAX_NEW_TOKENS` | `1024` | Max tokens to generate |
| `RESUMAP_SLIDING_WINDOW_OVERLAP` | `128` | Token overlap between chunks |
| `RESUMAP_CORS_ORIGINS` | `["*"]` | Allowed CORS origins |

## API Docs

Once running, interactive docs are available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`