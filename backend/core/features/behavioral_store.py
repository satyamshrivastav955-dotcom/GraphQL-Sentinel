"""
Behavioral Feature Store
Tracks client behavior patterns for anomaly detection.
"""
import time
from collections import defaultdict, deque
from typing import Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class BehavioralStore:
    """
    In-memory store for tracking client behavior patterns.
    Tracks query rates, error rates, and patterns per client.
    """
    
    def __init__(self, window_seconds: int = 60, max_history: int = 100):
        """
        Initialize behavioral store.
        
        Args:
            window_seconds: Time window for rate calculations
            max_history: Maximum number of queries to track per client
        """
        self.window_seconds = window_seconds
        self.max_history = max_history
        
        # client_id -> deque of (timestamp, query_hash, is_error)
        self.client_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        
        # client_id -> set of IPs
        self.client_ips: Dict[str, set] = defaultdict(set)
    
    def record_query(self, client_id: str, query: str, ip: str, is_error: bool = False):
        """
        Record a query from a client.
        
        Args:
            client_id: Unique client identifier
            query: GraphQL query string
            ip: Client IP address
            is_error: Whether the query resulted in an error
        """
        timestamp = time.time()
        query_hash = hash(query)
        
        # Add to history
        self.client_history[client_id].append((timestamp, query_hash, is_error))
        
        # Track IP
        self.client_ips[client_id].add(ip)
    
    def get_features(self, client_id: str) -> dict:
        """
        Extract behavioral features for a client.
        
        Args:
            client_id: Client identifier
            
        Returns:
            Dictionary of behavioral features
        """
        history = self.client_history.get(client_id, deque())
        
        if not history:
            return {
                'query_rate': 0.0,
                'error_rate': 0.0,
                'unique_ip_count': 1,
                'repeated_pattern_score': 0.0,
                'request_frequency': 0.0,
            }
        
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds
        
        # Filter to queries within window
        recent_queries = [(ts, qh, err) for ts, qh, err in history if ts >= cutoff_time]
        
        if not recent_queries:
            return {
                'query_rate': 0.0,
                'error_rate': 0.0,
                'unique_ip_count': len(self.client_ips.get(client_id, set())),
                'repeated_pattern_score': 0.0,
                'request_frequency': 0.0,
            }
        
        # Calculate query rate (queries per second)
        query_count = len(recent_queries)
        time_span = current_time - recent_queries[0][0] if len(recent_queries) > 1 else self.window_seconds
        query_rate = query_count / max(time_span, 1.0)
        
        # Calculate error rate
        error_count = sum(1 for _, _, is_err in recent_queries if is_err)
        error_rate = error_count / query_count if query_count > 0 else 0.0
        
        # Calculate repeated pattern score (same query hash repeatedly)
        query_hashes = [qh for _, qh, _ in recent_queries]
        unique_hashes = len(set(query_hashes))
        if unique_hashes > 0:
            # High score if many repeated queries
            repeated_pattern_score = 1.0 - (unique_hashes / query_count)
        else:
            repeated_pattern_score = 0.0
        
        # Request frequency (inverse of average time between requests)
        if len(recent_queries) > 1:
            time_diffs = [recent_queries[i][0] - recent_queries[i-1][0] 
                          for i in range(1, len(recent_queries))]
            avg_time_diff = sum(time_diffs) / len(time_diffs)
            request_frequency = 1.0 / max(avg_time_diff, 0.001)  # Avoid division by zero
        else:
            request_frequency = 0.0
        
        return {
            'query_rate': min(query_rate, 100.0),  # Cap at 100 qps
            'error_rate': error_rate,
            'unique_ip_count': len(self.client_ips.get(client_id, set())),
            'repeated_pattern_score': repeated_pattern_score,
            'request_frequency': min(request_frequency, 50.0),  # Cap at 50
        }
    
    def cleanup_old_data(self, max_age_seconds: int = 3600):
        """
        Remove data older than max_age_seconds.
        
        Args:
            max_age_seconds: Maximum age of data to keep
        """
        current_time = time.time()
        cutoff_time = current_time - max_age_seconds
        
        for client_id in list(self.client_history.keys()):
            history = self.client_history[client_id]
            
            # Remove old entries
            while history and history[0][0] < cutoff_time:
                history.popleft()
            
            # Remove empty histories
            if not history:
                del self.client_history[client_id]
                if client_id in self.client_ips:
                    del self.client_ips[client_id]
