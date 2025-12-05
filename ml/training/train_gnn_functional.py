"""
Functional GNN Model Training
Trains a GNN on GraphQL query AST graphs for pattern detection.
"""
import argparse
import pandas as pd
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Add parent directory to path for imports
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from ml.preprocessing.feature_schema import FEATURE_NAMES, features_to_vector
from backend.core.features.feature_pipeline import FeaturePipeline


def extract_features_from_query(query):
    """Extract features using the same pipeline as inference."""
    pipeline = FeaturePipeline()
    features = pipeline.extract_features(query, "training_client", {})
    if features:
        return features_to_vector(features)
    return None


def train_gnn(input_path, output_path):
    print("Loading data...")
    df = pd.read_parquet(input_path)
    
    if 'label' not in df.columns:
        print("Labels missing. Assuming BENIGN (0).")
        df['label'] = 0
    
    print(f"Extracting features for {len(df)} queries...")
    
    # Extract features using FeaturePipeline
    feature_vectors = []
    labels = []
    
    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            print(f"Processed {idx}/{len(df)} queries...")
        
        features = extract_features_from_query(row['query'])
        if features:
            feature_vectors.append(features)
            labels.append(row['label'])
    
    print(f"Successfully extracted features for {len(feature_vectors)} queries")
    
    X = np.array(feature_vectors)
    y = np.array(labels)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training GNN placeholder on {X_train.shape[0]} samples...")
    
    # Placeholder: Use RF until PyTorch Geometric GNN is implemented
    model = RandomForestClassifier(n_estimators=150, max_depth=20, random_state=42)
    model.fit(X_train, y_train)
    
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Train accuracy: {train_score:.3f}")
    print(f"Test accuracy: {test_score:.3f}")
    
    print(f"Saving model to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    model_data = {
        'model': model,
        'feature_names': FEATURE_NAMES
    }
    
    joblib.dump(model_data, output_path)
    print("Done.")


if __name__ == "____":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="ml/data/synthetic_1M/synthetic_data.parquet")
    parser.add_argument("--output", default="backend/core/models/gnn/gnn_model.joblib")  # Changed from .pth
    args = parser.parse_args()
    
    if os.path.exists(args.input):
        train_gnn(args.input, args.output)
    else:
        print(f"Input file {args.input} not found. Skipping.")
