import json
import time
import logging
import uuid
from datetime import datetime
from ..core.features.feature_pipeline import FeaturePipeline
from ..core.features.behavioral import set_behavioral_store
from ..core.features.behavioral_store import BehavioralStore
from ..core.security_engine.scorer import SecurityScorer
from ..core.security_engine.policy import SecurityPolicy
from ..core.security_engine.explainability import ExplainabilityEngine

logger = logging.getLogger(__name__)

class GraphQLGateway:
    def __init__(self, config: dict, model_paths: dict):
        self.config = config
        self.feature_pipeline = FeaturePipeline()
        self.scorer = SecurityScorer(model_paths, config)  # Pass config
        self.policy = SecurityPolicy(config.get('security', {}).get('policy', {}))
        self.explainer = ExplainabilityEngine()
        self.log_path = config.get('logging', {}).get('save_path', 'backend/storage/logs/decisions.jsonl')
        
        # Initialize behavioral store
        self.behavioral_store = BehavioralStore(window_seconds=60, max_history=100)
        set_behavioral_store(self.behavioral_store)
        
        # Log counter for unique IDs
        self.log_counter = 0

    async def process_request(self, request_data: dict, client_info: dict):
        start_time = time.time()
        query = request_data.get('query')
        
        if not query:
            return {"errors": [{"message": "No query provided"}]}

        try:
            # 1. Feature Extraction
            client_id = client_info.get('client_id', 'unknown')
            ip = client_info.get('ip', 'unknown')
            
            features = self.feature_pipeline.extract_features(query, client_id, {})
            
            if not features:
                return {"errors": [{"message": "Invalid GraphQL Query"}]}
    
            # 2. Scoring
            scores = self.scorer.score(features)
            
            # 3. Policy Decision
            decision = self.policy.decide(scores)
            
            # 4. Explanation
            explanations = self.explainer.explain(features, scores)
            
            # 5. Record in behavioral store
            is_error = decision == "BLOCK"
            self.behavioral_store.record_query(client_id, query, ip, is_error)
            
            # 6. Logging with unique ID
            self.log_counter += 1
            log_entry = {
                "id": str(uuid.uuid4()),  # Unique ID for each log
                "index": self.log_counter,  # Sequential index
                "timestamp": datetime.now().isoformat(),
                "client_id": client_id,
                "ip": ip,
                "query": query,
                "features": features,
                "scores": scores,
                "decision": decision,
                "explanations": explanations,
                "latency_ms": (time.time() - start_time) * 1000
            }
            self._log_decision(log_entry)
            
            # 7. Action
            if decision == "BLOCK":
                return {
                    "data": None,
                    "errors": [{"message": "Query blocked by Security Policy"}],
                    "extensions": {
                        "security": {
                            "decision": "BLOCK",
                            "risk_tier": scores.get('risk_tier', 'CRITICAL'),
                            "score": scores.get('ensemble_score'),
                            "model_scores": {
                                "autoencoder": scores.get('autoencoder', 0),
                                "random_forest": scores.get('random_forest', 0),
                                "lstm": scores.get('lstm', 0),
                                "gnn": scores.get('gnn', 0)
                            },
                            "latency_ms": (time.time() - start_time) * 1000
                        }
                    }
                }
            
            # Simulate forwarding to backend
            # In a real app, we would post to the actual GraphQL server here
            # For demo, we return a mock success response
            return {
                "data": {"message": "Query allowed and processed"},
                "extensions": {
                    "security": {
                        "decision": decision,
                        "risk_tier": scores.get('risk_tier', 'UNKNOWN'),
                        "score": scores.get('ensemble_score'),
                        "model_scores": {
                            "autoencoder": scores.get('autoencoder', 0),
                            "random_forest": scores.get('random_forest', 0),
                            "lstm": scores.get('lstm', 0),
                            "gnn": scores.get('gnn', 0)
                        },
                        "explanations": explanations,
                        "latency_ms": (time.time() - start_time) * 1000
                    }
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing request: {e}", exc_info=True)
            return {
                "errors": [{"message": "Internal security system error"}],
                "extensions": {
                    "security": {
                        "error": str(e),
                        "latency_ms": (time.time() - start_time) * 1000
                    }
                }
            }

    def _log_decision(self, entry):
        # Append to JSONL file
        try:
            with open(self.log_path, 'a') as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"Failed to log decision: {e}")
