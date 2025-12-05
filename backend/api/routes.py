from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import os
import asyncio
from datetime import datetime, timedelta
from collections import defaultdict
from .gateway import GraphQLGateway


router = APIRouter()
gateway = None  # Initialized in main startup

LOG_PATH = "backend/storage/logs/decisions.jsonl"


class GraphQLRequest(BaseModel):
    query: str
    variables: Optional[Dict[str, Any]] = None
    operationName: Optional[str] = None


def read_all_logs():
    """Read all logs from the JSONL file."""
    logs = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as f:
            for line in f:
                try:
                    logs.append(json.loads(line.strip()))
                except:
                    pass
    return logs


@router.post("/graphql-proxy")
async def graphql_proxy(request: Request, body: GraphQLRequest):
    if not gateway:
        raise HTTPException(status_code=503, detail="Gateway not initialized")
    
    client_info = {
        "client_id": request.headers.get("X-Client-ID", "unknown"),
        "ip": request.client.host,
        "user_agent": request.headers.get("User-Agent", "unknown")
    }
    
    result = await gateway.process_request(body.model_dump(), client_info)
    return result


@router.get("/api/stream")
async def get_stream():
    """Return last N logs for the live stream."""
    logs = read_all_logs()
    return logs[-50:] if len(logs) > 50 else logs


@router.get("/api/live")
async def live_stream():
    """SSE endpoint for real-time log streaming."""
    async def event_generator():
        last_count = 0
        while True:
            logs = read_all_logs()
            current_count = len(logs)
            
            if current_count > last_count:
                # Send new logs
                new_logs = logs[last_count:]
                for log in new_logs:
                    yield f"data: {json.dumps(log)}\n\n"
                last_count = current_count
            
            await asyncio.sleep(1)  # Check every second
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
        }
    )


@router.get("/api/metrics")
async def get_metrics():
    """Comprehensive metrics for the dashboard."""
    logs = read_all_logs()
    
    if not logs:
        return {
            "total_queries": 0,
            "blocked_count": 0,
            "throttled_count": 0,
            "high_risk_count": 0,
            "avg_threat_score": 0,
            "active_clients": 0,
            "avg_latency": 0,
            "attack_rate": 0,
            "threat_distribution": {
                "SAFE": 0, "LOW_RISK": 0, "MEDIUM_RISK": 0, "HIGH_RISK": 0, "CRITICAL": 0
            },
            "feature_importance": [],
            "load_over_time": [],
            "risk_trend": [],
            "threat_scores_timeline": []
        }
    
    # Basic counts
    total_queries = len(logs)
    blocked = sum(1 for l in logs if l.get('decision') == 'BLOCK')
    throttled = sum(1 for l in logs if l.get('decision') == 'THROTTLE')
    
    # Risk tier counts
    tier_counts = defaultdict(int)
    for log in logs:
        tier = log.get('scores', {}).get('risk_tier', 'SAFE')
        tier_counts[tier] += 1
    
    high_risk = tier_counts.get('HIGH_RISK', 0) + tier_counts.get('CRITICAL', 0)
    
    # Average threat score
    scores = [l.get('scores', {}).get('ensemble_score', 0) for l in logs]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    # Active clients
    clients = set(l.get('client_id', 'unknown') for l in logs)
    unique_ips = set(l.get('ip', 'unknown') for l in logs)
    
    # Average latency
    latencies = [l.get('latency_ms', 0) for l in logs]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    
    # Threat distribution for pie chart
    threat_distribution = {
        "SAFE": tier_counts.get('SAFE', 0),
        "LOW_RISK": tier_counts.get('LOW_RISK', 0),
        "MEDIUM_RISK": tier_counts.get('MEDIUM_RISK', 0),
        "HIGH_RISK": tier_counts.get('HIGH_RISK', 0),
        "CRITICAL": tier_counts.get('CRITICAL', 0)
    }
    
    # Feature importance (aggregate from explanations)
    feature_scores = defaultdict(float)
    feature_counts = defaultdict(int)
    for log in logs:
        for exp in log.get('explanations', []):
            feature = exp.get('feature', 'unknown')
            score = exp.get('score', 0)
            feature_scores[feature] += score
            feature_counts[feature] += 1
    
    # Also aggregate from features for more data
    feature_keys = ['max_depth', 'field_count', 'alias_count', 'introspection_score', 
                    'sensitive_field_count', 'mutation_score', 'complexity_score']
    for log in logs:
        features = log.get('features', {})
        for key in feature_keys:
            val = features.get(key, 0)
            if val > 0:
                feature_scores[key] += val
                feature_counts[key] += 1
    
    feature_importance = [
        {"feature": k, "impact": feature_scores[k] / feature_counts[k] if feature_counts[k] > 0 else 0, "count": feature_counts[k]}
        for k in feature_scores.keys()
    ]
    feature_importance.sort(key=lambda x: x['impact'], reverse=True)
    
    # Load over time (group by minute)
    load_by_minute = defaultdict(lambda: {"total": 0, "allowed": 0, "blocked": 0, "throttled": 0})
    for log in logs:
        ts = log.get('timestamp', '')
        try:
            dt = datetime.fromisoformat(ts)
            minute_key = dt.strftime('%H:%M')
            load_by_minute[minute_key]["total"] += 1
            decision = log.get('decision', 'ALLOW')
            if decision == 'ALLOW':
                load_by_minute[minute_key]["allowed"] += 1
            elif decision == 'BLOCK':
                load_by_minute[minute_key]["blocked"] += 1
            elif decision == 'THROTTLE':
                load_by_minute[minute_key]["throttled"] += 1
        except:
            pass
    
    load_over_time = [{"time": k, **v} for k, v in sorted(load_by_minute.items())[-20:]]
    
    # Risk trend over time
    risk_by_minute = defaultdict(lambda: {"SAFE": 0, "LOW_RISK": 0, "MEDIUM_RISK": 0, "HIGH_RISK": 0, "CRITICAL": 0})
    for log in logs:
        ts = log.get('timestamp', '')
        tier = log.get('scores', {}).get('risk_tier', 'SAFE')
        try:
            dt = datetime.fromisoformat(ts)
            minute_key = dt.strftime('%H:%M')
            risk_by_minute[minute_key][tier] += 1
        except:
            pass
    
    risk_trend = [{"time": k, **v} for k, v in sorted(risk_by_minute.items())[-20:]]
    
    # Threat scores timeline
    threat_scores_timeline = []
    for log in logs[-100:]:  # Last 100 entries
        ts = log.get('timestamp', '')
        score = log.get('scores', {}).get('ensemble_score', 0)
        try:
            dt = datetime.fromisoformat(ts)
            threat_scores_timeline.append({
                "time": dt.strftime('%H:%M:%S'),
                "score": round(score, 2)
            })
        except:
            pass
    
    return {
        "total_queries": total_queries,
        "blocked_count": blocked,
        "throttled_count": throttled,
        "high_risk_count": high_risk,
        "avg_threat_score": round(avg_score, 2),
        "active_clients": len(clients) + len(unique_ips) - 1,  # Unique entities
        "avg_latency": round(avg_latency, 2),
        "attack_rate": round(blocked / total_queries, 4) if total_queries > 0 else 0,
        "threat_distribution": threat_distribution,
        "feature_importance": feature_importance[:10],
        "load_over_time": load_over_time,
        "risk_trend": risk_trend,
        "threat_scores_timeline": threat_scores_timeline
    }


@router.get("/api/query/{query_id}")
async def get_query_details(query_id: str):
    """Get detailed information about a specific query by ID."""
    logs = read_all_logs()
    
    # Find log by ID
    log = None
    log_index = -1
    for idx, entry in enumerate(logs):
        if entry.get('id') == query_id:
            log = entry
            log_index = idx
            break
    
    if not log:
        raise HTTPException(status_code=404, detail="Query not found")
    
    # Get client behavior (last 10 scores from same client)
    client_id = log.get('client_id', 'unknown')
    client_logs = [l for l in logs if l.get('client_id') == client_id][-10:]
    client_timeline = [
        {
            "time": l.get('timestamp', '')[-8:],  # HH:MM:SS
            "score": l.get('scores', {}).get('ensemble_score', 0)
        }
        for l in client_logs
    ]
    
    return {
        "id": log.get('id'),
        "index": log_index,
        "timestamp": log.get('timestamp'),
        "client_id": log.get('client_id'),
        "ip": log.get('ip'),
        "query": log.get('query'),
        "features": log.get('features', {}),
        "scores": log.get('scores', {}),
        "decision": log.get('decision'),
        "explanations": log.get('explanations', []),
        "latency_ms": log.get('latency_ms'),
        "client_timeline": client_timeline
    }


@router.get("/api/explain/{query_id}")
async def get_explanation(query_id: str):
    """Get explainability data for a specific query by ID."""
    logs = read_all_logs()
    
    # Find log by ID
    log = None
    for entry in logs:
        if entry.get('id') == query_id:
            log = entry
            break
    
    if not log:
        raise HTTPException(status_code=404, detail="Query not found")
    
    # Build feature contributions
    features = log.get('features', {})
    explanations = log.get('explanations', [])
    
    # Create contribution bars from features
    contributions = []
    for exp in explanations:
        contributions.append({
            "feature": exp.get('feature'),
            "contribution": exp.get('score', 0) * 100,  # Scale to percentage
            "description": exp.get('description', '')
        })
    
    # Add inferred contributions from feature values
    feature_weights = {
        'max_depth': 3.0,
        'introspection_score': 15.0,
        'sensitive_field_count': 5.0,
        'mutation_score': 8.0,
        'alias_count': 2.0,
        'complexity_score': 1.0,
        'field_count': 0.5
    }
    
    for feat, weight in feature_weights.items():
        val = features.get(feat, 0)
        if val > 0:
            contribution = min(val * weight, 25)  # Cap at 25
            if not any(c['feature'] == feat for c in contributions):
                contributions.append({
                    "feature": feat,
                    "contribution": round(contribution, 1),
                    "description": f"{feat}: {val}"
                })
    
    contributions.sort(key=lambda x: x['contribution'], reverse=True)
    
    return {
        "id": log.get('id'),
        "ensemble_score": log.get('scores', {}).get('ensemble_score', 0),
        "risk_tier": log.get('scores', {}).get('risk_tier', 'SAFE'),
        "model_scores": {
            "autoencoder": log.get('scores', {}).get('autoencoder', 0),
            "random_forest": log.get('scores', {}).get('random_forest', 0),
            "lstm": log.get('scores', {}).get('lstm', 0),
            "gnn": log.get('scores', {}).get('gnn', 0)
        },
        "contributions": contributions[:5]  # Top 5
    }
