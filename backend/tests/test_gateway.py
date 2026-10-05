import asyncio
import json

import pytest

from backend.api.gateway import GraphQLGateway
from backend.core.security_engine.policy import SecurityPolicy


def make_gateway(tmp_path, config=None):
    cfg = {"logging": {"save_path": str(tmp_path / "decisions.jsonl")}}
    if config:
        cfg.update(config)
    return GraphQLGateway(cfg, {})


def process(gw, request_data, client_info=None):
    return asyncio.run(
        gw.process_request(request_data, client_info or {"client_id": "test", "ip": "127.0.0.1"})
    )


def test_gateway_allows_normal_query(tmp_path):
    gw = make_gateway(tmp_path)
    result = process(gw, {"query": "query { user { name } }"})
    assert result["data"] is not None
    assert result["extensions"]["security"]["decision"] == "ALLOW"
    assert result["extensions"]["security"]["risk_tier"] == "SAFE"


def test_gateway_blocks_critical_query(tmp_path):
    gw = make_gateway(tmp_path)
    # Introspection + mutation + sensitive field = multi-vector critical attack
    attack = 'mutation { login(user: "attacker") { password __typename } }'
    result = process(gw, {"query": attack})
    assert result["data"] is None
    assert result["errors"]
    assert result["extensions"]["security"]["decision"] == "BLOCK"
    assert result["extensions"]["security"]["risk_tier"] == "CRITICAL"


def test_gateway_rejects_missing_query(tmp_path):
    gw = make_gateway(tmp_path)
    result = process(gw, {})
    assert result["errors"]
    assert "query" in result["errors"][0]["message"].lower()


def test_gateway_rejects_non_string_query(tmp_path):
    gw = make_gateway(tmp_path)
    result = process(gw, {"query": 12345})
    assert result["errors"]
    assert "Internal" not in result["errors"][0]["message"]


def test_gateway_rejects_whitespace_query(tmp_path):
    gw = make_gateway(tmp_path)
    result = process(gw, {"query": "   "})
    assert result["errors"]


def test_gateway_redacts_internal_errors(tmp_path, monkeypatch):
    gw = make_gateway(tmp_path)

    def boom(*args, **kwargs):
        raise RuntimeError("sekret internal detail: db password=hunter2")

    monkeypatch.setattr(gw.feature_pipeline, "extract_features", boom)
    result = process(gw, {"query": "query { user { name } }"})
    assert result["errors"][0]["message"] == "Internal security system error"
    # Internal exception details must never reach the client
    assert "sekret" not in json.dumps(result)
    assert "hunter2" not in json.dumps(result)


def test_gateway_writes_decision_log(tmp_path):
    gw = make_gateway(tmp_path)
    process(gw, {"query": "query { user { name } }"})
    log_file = tmp_path / "decisions.jsonl"
    assert log_file.exists()
    lines = [line for line in log_file.read_text().splitlines() if line.strip()]
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["decision"] == "ALLOW"
    assert entry["client_id"] == "test"
    assert "latency_ms" in entry


def test_gateway_logs_into_configured_subdirectory(tmp_path):
    # save_path points into a directory that does not exist yet
    log_path = tmp_path / "logs" / "sub" / "decisions.jsonl"
    gw = GraphQLGateway({"logging": {"save_path": str(log_path)}}, {})
    process(gw, {"query": "query { user { name } }"})
    assert log_path.exists()


@pytest.mark.parametrize(
    "tier,expected",
    [
        ("SAFE", "ALLOW"),
        ("LOW_RISK", "ALLOW"),
        ("MEDIUM_RISK", "ALLOW"),
        ("HIGH_RISK", "THROTTLE"),
        ("CRITICAL", "BLOCK"),
    ],
)
def test_policy_decision_mapping(tier, expected):
    policy = SecurityPolicy({})
    assert policy.decide({"risk_tier": tier, "ensemble_score": 50}) == expected
