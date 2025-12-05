import pytest
from backend.core.parser.ast_parser import ASTParser
from backend.core.features.feature_pipeline import FeaturePipeline
from backend.core.security_engine.scorer import SecurityScorer

def test_ast_parser_valid():
    query = "query { user { name } }"
    ast = ASTParser.parse_query(query)
    assert ast is not None

def test_ast_parser_invalid():
    query = "query { user { name " # Missing brace
    ast = ASTParser.parse_query(query)
    assert ast is None

def test_feature_pipeline():
    pipeline = FeaturePipeline()
    query = "query { user { name } }"
    features = pipeline.extract_features(query)
    
    assert features is not None
    assert "field_count" in features
    # structural.py returns 'max_depth'
    assert "max_depth" in features
    assert features["max_depth"] > 0

def test_scorer_mock():
    # Test scorer with empty model paths (should use fallback/mock)
    scorer = SecurityScorer({})
    features = {
        "max_depth": 5,
        "introspection_score": 0,
        "sensitive_field_count": 0
    }
    scores = scorer.score(features)
    
    assert "ensemble_score" in scores
    assert 0 <= scores["ensemble_score"] <= 100
