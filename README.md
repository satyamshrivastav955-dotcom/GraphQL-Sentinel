# GraphQL Sentinel

A complete system for GraphQL security monitoring, anomaly detection, and blocking.

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional, for containerized run)

### Installation

1. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Install Frontend Dependencies**
   ```bash
   cd dashboard
   npm install
   ```

### Running the System

The anomaly-detection models (autoencoder, random forest, ensemble) ship
pre-trained in `backend/core/models/`, so no separate training step is needed.

#### 1. Run Backend
Start the FastAPI server **from the repository root** (the app imports the
`backend` package):
```bash
uvicorn backend.main:app --reload --port 8000
```

#### 2. Run Dashboard
Start the React frontend.
```bash
cd dashboard
npm start
```

### Docker Run
Alternatively, run everything with Docker Compose:
```bash
docker-compose up --build
```

### Running Tests
Backend unit tests (parser, feature pipeline, scorer, gateway, policy):
```bash
pip install -r backend/requirements.txt
pip install pytest
python -m pytest backend/tests -v
```
CI runs the same suite on every push and pull request (see
`.github/workflows/ci.yml`).

## Project Structure
- `backend/`: FastAPI application, security engine, and feature extraction.
- `backend/core/models/`: Pre-trained anomaly-detection models (joblib).
- `dashboard/`: React frontend for real-time monitoring.
- `backend/storage/`: Runtime decision logs (generated, not tracked in git).
