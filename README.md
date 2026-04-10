# AI Use Case Agents

A lightweight Python project that generates AI/ML proposals for a target company using a multi-agent pipeline powered by Google Gemini.

## What this project does

Given a company name, the app:

1. Researches the company and summarizes its industry context.
2. Generates 5 relevant AI/ML use cases.
3. Suggests supporting resources for each use case (GitHub repos, datasets, papers).
4. Returns a structured JSON proposal.

## Architecture

The core pipeline is implemented in `main.py` and split into three agents:

- **IndustryResearchAgent**: Produces company analysis.
- **UseCaseGenerationAgent**: Produces AI/ML use cases based on analysis.
- **ResourceAssetAgent**: Produces resource recommendations per use case.

`AIUseCaseGenerator` orchestrates all three asynchronously.

A Flask API in `flask_server.py` exposes the pipeline through a single endpoint.

## Tech stack

- Python 3.x
- Flask + Flask-CORS
- Google Generative AI SDK (`google-generativeai`)
- `python-dotenv` for local environment loading

## Project structure

```text
.
├── flask_server.py      # Flask API server
├── main.py              # Agent classes and orchestrator
├── requirements.txt     # Python dependencies
└── render.yaml          # Render deployment config
```

## Prerequisites

- Python 3.10+ (recommended)
- A valid Google AI API key

## Setup

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd ai-use-case-agents
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in a `.env` file:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Run the API server

```bash
python flask_server.py
```

Server default:

- URL: `http://127.0.0.1:5000`
- Port can be overridden via `PORT` env var.

## API usage

### Endpoint

`POST /proposal`

### Request body

```json
{
  "company_name": "Seagate"
}
```

### Example curl

```bash
curl -X POST http://127.0.0.1:5000/proposal \
  -H "Content-Type: application/json" \
  -d '{"company_name":"Seagate"}'
```

### Example response shape

```json
{
  "company_analysis": {
    "industry_sector": "...",
    "products_and_services": "...",
    "strategic_focus": "...",
    "tech_infrastructure": "...",
    "operational_challenges": "..."
  },
  "use_cases": [
    {
      "title": "...",
      "description": "...",
      "benefits": "...",
      "complexity": "High/Medium/Low",
      "roi_impact": "...",
      "technologies": "..."
    }
  ],
  "resources": {
    "<use_case_title>": {
      "github_repositories": ["..."],
      "datasets": ["..."],
      "research_papers": ["..."]
    }
  }
}
```

## Running the script directly (without Flask)

`main.py` includes an async entrypoint that runs a sample generation for `Seagate`:

```bash
python main.py
```

> Note: `main.py` currently reads the API key from `google_api_key` (lowercase), while `flask_server.py` expects `GOOGLE_API_KEY` (uppercase).

## Deployment (Render)

A ready-to-use `render.yaml` is included:

- Installs dependencies using `pip install -r requirements.txt`
- Starts service with `python flask_server.py`
- Expects `GOOGLE_API_KEY` as a secret env var

## Error handling behavior

The pipeline attempts to parse model output as JSON and falls back to safe placeholders when parsing fails. API-level validation includes:

- Missing/empty `company_name` → HTTP 400
- Missing `GOOGLE_API_KEY` → HTTP 500
- Runtime generation failures → HTTP 500

## License

Add your preferred license (e.g., MIT) in a `LICENSE` file.
