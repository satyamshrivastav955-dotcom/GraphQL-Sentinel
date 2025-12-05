import argparse
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def train_rf(input_path, output_path):
    print("Loading data...")
    df = pd.read_parquet(input_path)
    
    # If label is missing, assume benign (0)
    if 'label' not in df.columns:
        print("Labels missing in input data. Assuming BENIGN (0).")
        df['label'] = 0
        
    # Load synthetic data to get attacks
    synthetic_path = "ml/data/synthetic_1M/synthetic_data.parquet"
    if os.path.exists(synthetic_path):
        print(f"Loading synthetic data from {synthetic_path} to augment training...")
        df_syn = pd.read_parquet(synthetic_path)
        # Keep only attacks from synthetic data to mix with real benign data
        # Or keep all to have a mix of synthetic benign too
        df = pd.concat([df, df_syn], ignore_index=True)
    
    # Feature Engineering (Simulation)
    if 'depth' not in df.columns:
        df['depth'] = df['query'].apply(lambda x: str(x).count('{'))
        df['length'] = df['query'].apply(len)
        df['introspection'] = df['query'].apply(lambda x: 1 if '__schema' in str(x) else 0)
    
    features = ['depth', 'length', 'introspection']
    X = df[features]
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=200, max_depth=None, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    
    print("Evaluating...")
    y_pred = rf.predict(X_test)
    print(classification_report(y_test, y_pred))
    
    print(f"Saving model to {output_path}")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    joblib.dump(rf, output_path)
    print("Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="ml/data/synthetic_1M/synthetic_data.parquet")
    parser.add_argument("--output", default="backend/core/models/random_forest/rf_model.joblib")
    args = parser.parse_args()
    
    if os.path.exists(args.input):
        train_rf(args.input, args.output)
    else:
        print(f"Input file {args.input} not found. Skipping.")
