import logging
try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    
logger = logging.getLogger(__name__)

class ExplainabilityEngine:
    def __init__(self):
        self.explainer = None
        self.feature_names = [
            'max_depth', 'field_count', 'alias_count', 'fragment_count',
            'directive_count', 'introspection_score', 'sensitive_field_count',
            'mutation_score', 'complexity_score', 'token_count', 'query_length',
            'query_rate', 'error_rate', 'unique_ip_count'
        ]

    def explain(self, features: dict, scores: dict, model=None) -> list:
        """
        Generate explanations for model predictions.
        Uses SHAP if available and model provided, otherwise heuristics.
        """
        explanations = []
        
        # Try SHAP if available and model is Random Forest
        if SHAP_AVAILABLE and model is not None and hasattr(model, 'predict_proba'):
            try:
                # Prepare feature vector in correct order
                feature_vector = [features.get(name, 0) for name in self.feature_names[:3]]  # depth, length, introspection
                
                # Initialize explainer only once
                if self.explainer is None:
                    self.explainer = shap.TreeExplainer(model)
                
                # Calculate SHAP values
                shap_values = self.explainer.shap_values([feature_vector])
                
                # Get SHAP values for the positive class (class 1 - attack)
                if isinstance(shap_values, list) and len(shap_values) > 1:
                    shap_vals = shap_values[1][0]  # Class 1 values
                else:
                    shap_vals = shap_values[0]
                
                # Create explanations from top SHAP values
                for idx, val in enumerate(shap_vals):
                    if abs(val) > 0.01:  # Only significant contributions
                        feat_name = self.feature_names[idx] if idx < len(self.feature_names) else f"feature_{idx}"
                        explanations.append({
                            "feature": feat_name,
                            "score": float(abs(val)),
                            "description": f"{'Increases' if val > 0 else 'Decreases'} risk score"
                        })
                
                explanations.sort(key=lambda x: x['score'], reverse=True)
                
                if len(explanations) > 0:
                    return explanations[:5]  # Top 5
                    
            except Exception as e:
                logger.debug(f"SHAP explanation failed: {e}, falling back to heuristics")
        
        # Fallback to heuristic explanations
        if features.get('introspection_score', 0) > 0:
            explanations.append({
                "feature": "introspection_score",
                "score": 0.8,
                "description": "Introspection query detected - exposes schema"
            })
            
        if features.get('max_depth', 0) > 10:
            explanations.append({
                "feature": "max_depth",
                "score": 0.7,
                "description": f"Deeply nested query (depth={features['max_depth']}) - DoS risk"
            })
        elif features.get('max_depth', 0) > 8:
            explanations.append({
                "feature": "max_depth",
                "score": 0.5,
                "description": f"Moderately deep nesting (depth={features['max_depth']})"
            })
            
        if features.get('alias_count', 0) > 5:
            explanations.append({
                "feature": "alias_count",
                "score": 0.6,
                "description": f"Excessive aliases ({features['alias_count']}) - batching attack"
            })
            
        if features.get('sensitive_field_count', 0) > 0:
            explanations.append({
                "feature": "sensitive_field_count",
                "score": 0.65,
                "description": f"Accessing {features['sensitive_field_count']} sensitive field(s)"
            })
            
        if features.get('mutation_score', 0) > 0:
            explanations.append({
                "feature": "mutation_score",
                "score": 0.55,
                "description": "Mutation operation detected"
            })
        
        if features.get('fragment_count', 0) > 2:
            explanations.append({
                "feature": "fragment_count",
                "score": 0.5,
                "description": f"Multiple fragments ({features['fragment_count']}) - complexity"
            })
        
        if features.get('query_rate', 0) > 10:
            explanations.append({
                "feature": "query_rate",
                "score": 0.6,
                "description": f"High query rate ({features['query_rate']:.1f} qps) - abuse"
            })
        
        explanations.sort(key=lambda x: x['score'], reverse=True)
        return explanations[:5]
