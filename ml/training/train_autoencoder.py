import argparse
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def train_autoencoder(input_path, output_path):
    print("Loading data...")
    df = pd.read_parquet(input_path)
    
    if 'label' not in df.columns:
        print("Labels missing. Assuming BENIGN (0).")
        df['label'] = 0
    
    # Filter for benign queries only for AE training
    benign_df = df[df['label'] == 0]
    
    # SIMULATION: Create dummy features if not present
    if 'depth' not in benign_df.columns:
        benign_df['depth'] = benign_df['query'].apply(lambda x: str(x).count('{'))
        benign_df['length'] = benign_df['query'].apply(len)
    
    features = ['depth', 'length']
    X = benign_df[features].values
    
    print("Training Autoencoder...")
    # Simple Autoencoder using MLPRegressor (Identity mapping)
    # Input -> Hidden -> Output (same as Input)
    ae = Pipeline([
        ('scaler', StandardScaler()),
        ('model', MLPRegressor(hidden_layer_sizes=(10, 5, 10), max_iter=500, random_state=42))
    ])
    
    ae.fit(X, X)
    
    print(f"Saving model to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(ae, output_path)
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="ml/data/synthetic_1M/synthetic_data.parquet")
    parser.add_argument("--output", default="backend/core/models/autoencoder/ae_model.joblib")
    args = parser.parse_args()
    
    if os.path.exists(args.input):
        train_autoencoder(args.input, args.output)
    else:
        print(f"Input file {args.input} not found. Skipping.")
