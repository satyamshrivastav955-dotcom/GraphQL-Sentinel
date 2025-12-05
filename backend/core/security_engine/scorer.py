import joblib
import os
import logging

logger = logging.getLogger(__name__)

class SecurityScorer:
    """
    Multi-Model Security Scorer for GraphQL Queries
    
    Implements 5-tier risk classification (config-driven):
    - SAFE (0-safe_threshold): Normal traffic
    - LOW RISK (safe_threshold+1 - low_risk_threshold): Heavy but normal
    - MEDIUM RISK (low_risk_threshold+1 - medium_risk_threshold): Suspicious
    - HIGH RISK (medium_risk_threshold+1 - high_risk_threshold): Likely attack
    - CRITICAL (high_risk_threshold+1 - 100): Confirmed attack
    """
    
    def __init__(self, model_paths: dict, config: dict = None):
        self.model_paths = model_paths
        self.config = config or {}
        self.models = {}
        
        # Load tier thresholds from config
        tier_config = self.config.get('security', {}).get('policy', {}).get('risk_tier_thresholds', {})
        self.tier_thresholds = {
            'safe': tier_config.get('safe', 20),
            'low_risk': tier_config.get('low_risk', 40),
            'medium_risk': tier_config.get('medium_risk', 65),
            'high_risk': tier_config.get('high_risk', 85),
        }
        
        self.load_models()

    def load_models(self):
        for name, path in self.model_paths.items():
            if os.path.exists(path):
                try:
                    self.models[name] = joblib.load(path)
                    logger.info(f"Loaded model {name} from {path}")
                except Exception as e:
                    logger.error(f"Failed to load model {name}: {e}")
            else:
                logger.warning(f"Model {name} not found at {path}. Using fallback.")

    def score(self, features: dict) -> dict:
        """
        Score a query based on extracted features.
        Returns scores from individual models and final ensemble score.
        """
        scores = {}
        
        # Extract key features
        depth = features.get('max_depth', 0)
        breadth = features.get('field_count', 0)
        length = features.get('query_length', 0)
        introspection = features.get('introspection_score', 0)
        alias_count = features.get('alias_count', 0)
        fragment_count = features.get('fragment_count', 0)
        directive_count = features.get('directive_count', 0)
        sensitive_fields = features.get('sensitive_field_count', 0)
        mutation_score = features.get('mutation_score', 0)
        cost_estimate = features.get('cost_estimate', 0)
        
        # ========== PURE HEURISTIC SCORING (More Reliable) ==========
        # Start with base score of 0
        base_score = 0.0
        
        # 1. INTROSPECTION CHECK (MEDIUM RISK minimum)
        if introspection > 0:
            base_score += 45  # Pushes to MEDIUM RISK
        
        # 2. DEPTH ANALYSIS
        if depth <= 3:
            base_score += 0  # Normal
        elif depth <= 5:
            base_score += 5  # Slightly concerning
        elif depth <= 8:
            base_score += 15 + (depth - 5) * 5  # Concerning
        elif depth <= 12:
            base_score += 30 + (depth - 8) * 8  # High risk
        else:
            base_score += 60 + (depth - 12) * 5  # Critical
        
        # 3. ALIAS ABUSE (Batching attack)
        if alias_count > 3:
            base_score += (alias_count - 3) * 5
        
        # 4. FIELD COUNT (Resource exhaustion)
        if breadth > 10:
            base_score += (breadth - 10) * 1
        
        # 5. SENSITIVE FIELD ACCESS
        if sensitive_fields > 0:
            base_score += sensitive_fields * 10
        
        # 6. MUTATION WITH SENSITIVE FIELDS
        if mutation_score > 0:
            base_score += 15
            if sensitive_fields > 0:
                base_score += 20  # Dangerous combo
        
        # 7. FRAGMENT ABUSE
        if fragment_count > 2:
            base_score += fragment_count * 8
        
        # 8. MULTI-VECTOR ATTACK DETECTION
        attack_signals = 0
        if introspection > 0: attack_signals += 1
        if depth > 8: attack_signals += 1
        if alias_count > 5: attack_signals += 1
        if fragment_count > 2: attack_signals += 1
        if sensitive_fields > 0: attack_signals += 1
        
        if attack_signals >= 3:
            base_score += 20  # Multi-vector attack confirmed
        
        # ========== ML MODEL SCORES (For reference, not primary driver) ==========
        # Autoencoder
        if 'autoencoder' in self.models:
            try:
                X_ae = [[depth, length]]
                X_pred = self.models['autoencoder'].predict(X_ae)
                mse = ((X_ae[0][0] - X_pred[0][0])**2 + (X_ae[0][1] - X_pred[0][1])**2) / 2
                scores['autoencoder'] = round(min(1.0, mse / 100), 3)
            except Exception as e:
                logger.debug(f"Autoencoder scoring error: {e}")
                scores['autoencoder'] = 0.0
        else:
            scores['autoencoder'] = 0.0

        # Random Forest
        if 'random_forest' in self.models:
            try:
                X_rf = [[depth, length, 1 if introspection > 0 else 0]]
                probs = self.models['random_forest'].predict_proba(X_rf)
                scores['random_forest'] = round(probs[0][1], 3)
            except Exception as e:
                logger.debug(f"Random Forest scoring error: {e}")
                scores['random_forest'] = 0.0
        else:
            scores['random_forest'] = 0.0

        # LSTM and GNN placeholders (TODO: implement)
        scores['lstm'] = 0.0
        scores['gnn'] = 0.0
        
        # ========== FINAL SCORE ==========
        final_score = min(100, max(0, base_score))
        scores['ensemble_score'] = round(final_score, 1)
        
        # ========== RISK TIER (Config-driven) ==========
        if final_score <= self.tier_thresholds['safe']:
            scores['risk_tier'] = 'SAFE'
        elif final_score <= self.tier_thresholds['low_risk']:
            scores['risk_tier'] = 'LOW_RISK'
        elif final_score <= self.tier_thresholds['medium_risk']:
            scores['risk_tier'] = 'MEDIUM_RISK'
        elif final_score <= self.tier_thresholds['high_risk']:
            scores['risk_tier'] = 'HIGH_RISK'
        else:
            scores['risk_tier'] = 'CRITICAL'
        
        logger.debug(f"Final Score={final_score}, Tier={scores['risk_tier']}")
        
        return scores
