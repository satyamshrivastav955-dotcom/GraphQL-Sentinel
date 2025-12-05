# Machine Learning Pipeline

This directory contains the data processing and model training pipeline for GraphQL Sentinel.

## Structure
- `data/`: Contains raw, synthetic, and processed data.
- `preprocessing/`: Scripts for data cleaning and feature extraction.
- `training/`: Scripts for training anomaly detection models.
- `experiments/`: Configuration and results of experiments.

## Usage
1. Generate synthetic data:
   ```bash
   python preprocessing/generate_synthetic.py
   ```
2. Train models:
   ```bash
   python training/train_autoencoder.py
   ```
