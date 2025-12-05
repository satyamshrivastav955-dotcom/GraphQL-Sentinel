import logging

logger = logging.getLogger(__name__)


class SecurityPolicy:
    """
    Security Policy Engine for GraphQL Sentinel
    
    Implements 5-tier policy actions:
    | Tier        | Action                    |
    |-------------|---------------------------|
    | SAFE        | ALLOW                     |
    | LOW_RISK    | ALLOW + LOG               |
    | MEDIUM_RISK | ALLOW + ALERT             |
    | HIGH_RISK   | THROTTLE + ALERT          |
    | CRITICAL    | BLOCK + ALERT             |
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.thresholds = config.get('thresholds', {})

    def decide(self, scores: dict) -> str:
        """
        Make a policy decision based on scores.
        Returns: ALLOW, THROTTLE, or BLOCK
        """
        risk_tier = scores.get('risk_tier', 'SAFE')
        ensemble_score = scores.get('ensemble_score', 0)
        
        logger.debug(f"Policy decision: Score={ensemble_score:.1f}, Tier={risk_tier}")
        
        # Map risk tier to action
        if risk_tier == 'SAFE':
            return "ALLOW"
        elif risk_tier == 'LOW_RISK':
            return "ALLOW"  # Logged separately
        elif risk_tier == 'MEDIUM_RISK':
            return "ALLOW"  # Alert triggered separately
        elif risk_tier == 'HIGH_RISK':
            return "THROTTLE"
        elif risk_tier == 'CRITICAL':
            return "BLOCK"
        else:
            return "ALLOW"
    
    def get_action_details(self, scores: dict) -> dict:
        """
        Get detailed action information including logging and alert flags.
        """
        risk_tier = scores.get('risk_tier', 'SAFE')
        decision = self.decide(scores)
        
        action_details = {
            'decision': decision,
            'risk_tier': risk_tier,
            'should_log': risk_tier != 'SAFE',
            'should_alert': risk_tier in ['MEDIUM_RISK', 'HIGH_RISK', 'CRITICAL'],
            'score': scores.get('ensemble_score', 0)
        }
        
        return action_details
