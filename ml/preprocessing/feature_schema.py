"""
Feature Schema - Single Source of Truth
Defines the exact features used for both training and inference.
"""

# Complete feature set extracted by FeaturePipeline
FEATURE_NAMES = [
    # Structural features (from AST)
    'max_depth',
    'field_count',
    'alias_count',
    'fragment_count',
    'directive_count',
    
    # Semantic features
    'introspection_score',
    'sensitive_field_count',
    'mutation_score',
    
    # Cost features
    'complexity_score',
    'token_count',
    
    # Query metadata
    'query_length',
    
    # Behavioral features (client-based)
    'query_rate',
    'error_rate',
    'unique_ip_count',
]

# Feature indices for quick lookup
FEATURE_INDICES = {name: idx for idx, name in enumerate(FEATURE_NAMES)}

# Number of features
NUM_FEATURES = len(FEATURE_NAMES)


def features_to_vector(features_dict: dict) -> list:
    """
    Convert feature dictionary to ordered vector matching FEATURE_NAMES.
    
    Args:
        features_dict: Dictionary of feature_name -> value
        
    Returns:
        List of feature values in correct order, with 0.0 for missing features
    """
    return [features_dict.get(name, 0.0) for name in FEATURE_NAMES]


def vector_to_features(vector: list) -> dict:
    """
    Convert feature vector back to dictionary.
    
    Args:
        vector: List of feature values
        
    Returns:
        Dictionary mapping feature names to values
    """
    return {name: vector[i] for i, name in enumerate(FEATURE_NAMES) if i < len(vector)}
