"""
COMPREHENSIVE SYSTEM VERIFICATION
Tests all 5 tiers with multiple queries each
"""
import sys
import os
sys.path.append(os.getcwd())

from backend.core.parser.ast_parser import ASTParser
from backend.core.features.feature_pipeline import FeaturePipeline
from backend.core.security_engine.scorer import SecurityScorer
from backend.core.security_engine.policy import SecurityPolicy

def run_full_verification():
    print("=" * 80)
    print("GRAPHQL SENTINEL - FULL SYSTEM VERIFICATION")
    print("=" * 80)
    
    # Initialize components
    pipeline = FeaturePipeline()
    model_paths = {
        "autoencoder": "backend/core/models/autoencoder/ae_model.joblib",
        "random_forest": "backend/core/models/random_forest/rf_model.joblib"
    }
    scorer = SecurityScorer(model_paths)
    policy = SecurityPolicy({"thresholds": {"ensemble_score": 20}})
    
    # Test cases: (Expected Tier, Query, Description)
    test_cases = [
        # SAFE (0-20)
        ("SAFE", "query { user { id } }", "Simple single field"),
        ("SAFE", "query { user { name email } }", "Two fields"),
        ("SAFE", "query { products { id title } }", "List query"),
        
        # LOW_RISK (21-40)
        ("LOW_RISK", "query { users { id name email phone address city country zipcode company } }", "Many fields"),
        ("LOW_RISK", "query { a { b { c { d { e { f } } } } } }", "Depth 6 - borderline"),
        
        # MEDIUM_RISK (41-65)
        ("MEDIUM_RISK", "query { __schema { types { name } } }", "Introspection"),
        ("MEDIUM_RISK", "query { __type(name: \"User\") { fields { name } } }", "Type introspection"),
        
        # HIGH_RISK (66-85)
        ("HIGH_RISK", "query { a { b { c { d { e { f { g { h { i { j } } } } } } } } } }", "Deep nesting (10 levels)"),
        ("HIGH_RISK", "query { u1:user{id} u2:user{id} u3:user{id} u4:user{id} u5:user{id} u6:user{id} u7:user{id} u8:user{id} }", "8 aliases"),
        
        # CRITICAL (86-100)
        ("CRITICAL", "query { __schema { types { name } } a { b { c { d { e { f { g { h { i } } } } } } } } }", "Introspection + Depth"),
        ("CRITICAL", "query { a { b { c { d { e { f { g { h { i { j { k { l { m { n { o } } } } } } } } } } } } } } }", "Extreme depth (15)"),
    ]
    
    results = {"PASS": 0, "FAIL": 0}
    failed_tests = []
    
    print("\n" + "-" * 80)
    print("RUNNING TESTS...")
    print("-" * 80)
    
    for expected_tier, query, description in test_cases:
        # Parse and extract features
        features = pipeline.extract_features(query)
        if not features:
            print(f"✗ PARSE ERROR: {description}")
            results["FAIL"] += 1
            failed_tests.append((expected_tier, description, "PARSE_ERROR", 0))
            continue
        
        # Score
        scores = scorer.score(features)
        actual_tier = scores.get('risk_tier', 'UNKNOWN')
        score = scores.get('ensemble_score', 0)
        
        # Policy decision
        decision = policy.decide(scores)
        
        # Check result
        if expected_tier == actual_tier:
            status = "✓ PASS"
            results["PASS"] += 1
        else:
            status = "✗ FAIL"
            results["FAIL"] += 1
            failed_tests.append((expected_tier, description, actual_tier, score))
        
        print(f"{status} | {description}")
        print(f"       Expected: {expected_tier}, Got: {actual_tier} (Score: {score:.1f}, Decision: {decision})")
        print()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Tests: {results['PASS'] + results['FAIL']}")
    print(f"Passed: {results['PASS']}")
    print(f"Failed: {results['FAIL']}")
    
    if failed_tests:
        print("\nFailed Tests:")
        for expected, desc, actual, score in failed_tests:
            print(f"  - {desc}: Expected {expected}, Got {actual} (Score: {score})")
    
    print("\n" + "=" * 80)
    print("TIER THRESHOLDS REFERENCE:")
    print("=" * 80)
    print("| Score   | Tier        | Action   |")
    print("|---------|-------------|----------|")
    print("| 0-20    | SAFE        | ALLOW    |")
    print("| 21-40   | LOW_RISK    | ALLOW    |")
    print("| 41-65   | MEDIUM_RISK | ALLOW    |")
    print("| 66-85   | HIGH_RISK   | THROTTLE |")
    print("| 86-100  | CRITICAL    | BLOCK    |")
    print("=" * 80)
    
    return results["FAIL"] == 0

if __name__ == "__main__":
    success = run_full_verification()
    exit(0 if success else 1)
