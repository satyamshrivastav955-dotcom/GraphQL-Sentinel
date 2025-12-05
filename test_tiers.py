import sys
import os
sys.path.append(os.getcwd())

from backend.core.parser.ast_parser import ASTParser
from backend.core.features.feature_pipeline import FeaturePipeline
from backend.core.security_engine.scorer import SecurityScorer

def test_queries():
    pipeline = FeaturePipeline()
    model_paths = {
        "autoencoder": "backend/core/models/autoencoder/ae_model.joblib",
        "random_forest": "backend/core/models/random_forest/rf_model.joblib"
    }
    scorer = SecurityScorer(model_paths)
    
    queries = [
        ("SAFE", "query { user { id name } }"),
        ("LOW_RISK", "query { users(limit: 100) { id name email address phone } }"),
        ("MEDIUM_RISK", "query { __schema { types { name } } }"),
        ("HIGH_RISK", "query { a { b { c { d { e { f { g { h { i { j { k } } } } } } } } } } }"),
        ("CRITICAL", "query { __schema { types { name } } a { b { c { d { e { f { g { h { i { j { k } } } } } } } } } } u1:user{id} u2:user{id} u3:user{id} u4:user{id} u5:user{id} u6:user{id} }"),
    ]
    
    print("=" * 80)
    print("TESTING 5-TIER CLASSIFICATION")
    print("=" * 80)
    
    for expected_tier, query in queries:
        print(f"\n--- Expected: {expected_tier} ---")
        print(f"Query: {query[:60]}...")
        
        features = pipeline.extract_features(query)
        if not features:
            print("ERROR: Failed to parse query")
            continue
            
        scores = scorer.score(features)
        actual_tier = scores.get('risk_tier', 'UNKNOWN')
        score = scores.get('ensemble_score', 0)
        
        status = "✓ PASS" if expected_tier == actual_tier else "✗ FAIL"
        print(f"Score: {score:.1f}, Tier: {actual_tier} {status}")

if __name__ == "__main__":
    test_queries()
