from .structural import extract_structural_features
from .semantic import extract_semantic_features
from .behavioral import extract_behavioral_features
from .cost_features import extract_cost_features
from ..parser.ast_parser import ASTParser

class FeaturePipeline:
    def __init__(self):
        pass

    def extract_features(self, query: str, client_id: str = None, context: dict = None) -> dict:
        if context is None:
            context = {}
            
        ast = ASTParser.parse_query(query)
        if not ast:
            return None

        features = {}
        
        # AST-based features
        features.update(extract_structural_features(ast))
        features.update(extract_semantic_features(ast))
        features.update(extract_cost_features(ast, query))  # Pass query string for token count
        
        # Behavioral features
        features.update(extract_behavioral_features(client_id, context))
        
        # Raw features
        features['query_length'] = len(query)
        
        return features
