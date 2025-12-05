from graphql.language.visitor import Visitor, visit
from graphql.language.ast import DocumentNode

class CostVisitor(Visitor):
    def __init__(self):
        super().__init__()
        self.complexity = 0

    def enter_field(self, node, key, parent, path, ancestors):
        # Simple cost model: 1 point per field + extra for arguments
        self.complexity += 1
        if node.arguments:
            self.complexity += len(node.arguments)

def extract_cost_features(ast: DocumentNode, query_string: str = "") -> dict:
    visitor = CostVisitor()
    visit(ast, visitor)
    
    # Calculate token count from query string
    token_count = len(query_string.split()) if query_string else 0
    
    return {
        "complexity_score": visitor.complexity,
        "token_count": token_count
    }
