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


def test_ring_buffer_operations():
    from backend.storage.ring_buffer import LogRingBuffer

    rb = LogRingBuffer(max_entries=3)
    rb.append({"id": "q1", "val": 1})
    rb.append({"id": "q2", "val": 2})
    rb.append({"id": "q3", "val": 3})

    assert rb.count() == 3
    assert rb.get_by_id("q1")["val"] == 1
    assert rb.get_by_id("q2")["val"] == 2

    # Overflow should evict q1
    rb.append({"id": "q4", "val": 4})
    assert rb.count() == 3
    assert rb.get_by_id("q1") is None
    assert rb.get_by_id("q4")["val"] == 4
    assert [e["id"] for e in rb.get_all()] == ["q2", "q3", "q4"]

