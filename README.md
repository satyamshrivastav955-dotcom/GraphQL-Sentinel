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

#### 1. Generate Synthetic Data
First, generate the synthetic dataset to train the models (or use as a fallback).
```bash
python ml/preprocessing/generate_synthetic.py --n 1000000 --seed 42
```

#### 2. Train Models
Train the anomaly detection models.
```bash
python ml/training/train_autoencoder.py
python ml/training/train_random_forest.py
# ... run other training scripts as needed
```

#### 3. Run Backend
Start the FastAPI server.
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### 4. Run Dashboard
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

## Project Structure
- `backend/`: FastAPI application, security engine, and feature extraction.
- `ml/`: Data preprocessing, synthetic generation, and training scripts.
- `dashboard/`: React frontend for real-time monitoring.
