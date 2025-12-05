import sys
import os
sys.path.append(os.getcwd())

from backend.core.parser.ast_parser import ASTParser
from backend.core.features.feature_pipeline import FeaturePipeline
from backend.core.security_engine.scorer import SecurityScorer

def test_single():
    pipeline = FeaturePipeline()
    model_paths = {
        "autoencoder": "backend/core/models/autoencoder/ae_model.joblib",
        "random_forest": "backend/core/models/random_forest/rf_model.joblib"
    }
    scorer = SecurityScorer(model_paths)
    
    query = "query { user { id name } }"
    print(f"Testing query: {query}")
    
    features = pipeline.extract_features(query)
    print(f"Features: {features}")
    
    scores = scorer.score(features)
    print(f"Scores: {scores}")

if __name__ == "__main__":
    test_single()
