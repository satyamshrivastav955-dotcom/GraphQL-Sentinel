from typing import Optional
from .behavioral_store import BehavioralStore

# Global behavioral store instance (imported by gateway)
_behavioral_store: Optional[BehavioralStore] = None


def set_behavioral_store(store: BehavioralStore):
    """Set the global behavioral store instance."""
    global _behavioral_store
    _behavioral_store = store


def extract_behavioral_features(client_id: str, context: dict) -> dict:
    """
    Extracts features based on client history.
    
    Args:
        client_id: Client identifier
        context: Additional context (not currently used, store tracks everything)
        
    Returns:
        Dictionary of behavioral features
    """
    if _behavioral_store is None:
        # Fallback if store not initialized
        return {
            "query_rate": 0.0,
            "error_rate": 0.0,
            "unique_ip_count": 1,
            "repeated_pattern_score": 0.0,
            "request_frequency": 0.0,
        }
    
    return _behavioral_store.get_features(client_id)
