import sys
import os
sys.path.append(os.getcwd())

from backend.core.features.feature_pipeline import FeaturePipeline
from backend.core.security_engine.scorer import SecurityScorer
from backend.core.security_engine.policy import SecurityPolicy

p = FeaturePipeline()
s = SecurityScorer({
    'autoencoder': 'backend/core/models/autoencoder/ae_model.joblib',
    'random_forest': 'backend/core/models/random_forest/rf_model.joblib'
})
policy = SecurityPolicy({})

tests = [
    ("SAFE", "query { user { id } }"),
    ("SAFE", "query { user { name email } }"),
    ("MEDIUM_RISK", "query { __schema { types { name } } }"),
    ("HIGH_RISK", "query { a { b { c { d { e { f { g { h { i { j } } } } } } } } } }"),
    ("CRITICAL", "query { __schema { types { name } } a { b { c { d { e { f { g { h { i } } } } } } } } }"),
]

print("=" * 60)
print("TIER VERIFICATION RESULTS")
print("=" * 60)

for expected, query in tests:
    features = p.extract_features(query)
    scores = s.score(features)
    decision = policy.decide(scores)
    
    tier = scores['risk_tier']
    score = scores['ensemble_score']
    
    status = "PASS" if expected == tier else "FAIL"
    print(f"[{status}] Expected: {expected:12} | Got: {tier:12} | Score: {score:5.1f} | Decision: {decision}")

print("=" * 60)
