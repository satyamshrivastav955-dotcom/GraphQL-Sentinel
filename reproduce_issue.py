import sys
import os
import asyncio
import json

# Add current directory to path so we can import backend
sys.path.append(os.getcwd())

from backend.core.parser.ast_parser import ASTParser
from backend.core.features.feature_pipeline import FeaturePipeline
from backend.core.security_engine.scorer import SecurityScorer
from backend.core.security_engine.policy import SecurityPolicy

async def test_scoring():
    print("--- STARTING REPRODUCTION TEST ---")
    
    query = """
    query {
      __schema {
        types {
          name
        }
      }
    }
    """
    print(f"Query: {query.strip()}")
    
    # 1. Test Parser
    print("\n1. Testing AST Parser...")
    ast = ASTParser.parse_query(query)
    if not ast:
        print("ERROR: AST Parser returned None")
        return
    print("AST Parsed successfully")

    # 2. Test Feature Pipeline
    print("\n2. Testing Feature Pipeline...")
    pipeline = FeaturePipeline()
    features = pipeline.extract_features(query)
    print(f"Extracted Features: {json.dumps(features, indent=2)}")
    
    if features.get('introspection_score', 0) == 0:
        print("FAILURE: Introspection score is 0! Expected > 0")
    else:
        print("SUCCESS: Introspection score detected")

    # 3. Test Scorer
    print("\n3. Testing Scorer...")
    # Mock model paths (files might not exist, but scorer handles fallbacks)
    model_paths = {
        "autoencoder": "backend/core/models/autoencoder/ae_model.joblib",
        "random_forest": "backend/core/models/random_forest/rf_model.joblib"
    }
    scorer = SecurityScorer(model_paths)
    scores = scorer.score(features)
    print(f"Scores: {json.dumps(scores, indent=2)}")
    
    if scores.get('ensemble_score', 0) < 20:
        print("FAILURE: Score is too low for an attack!")
    else:
        print("SUCCESS: Score is high enough")

    # 4. Test Policy
    print("\n4. Testing Policy...")
    config = {
        "thresholds": {
            "ensemble_score": 20
        }
    }
    policy = SecurityPolicy(config)
    decision = policy.decide(scores)
    print(f"Decision: {decision}")
    
    if decision != "BLOCK":
        print("FAILURE: Decision was not BLOCK")
    else:
        print("SUCCESS: Decision was BLOCK")

if __name__ == "__main__":
    asyncio.run(test_scoring())
