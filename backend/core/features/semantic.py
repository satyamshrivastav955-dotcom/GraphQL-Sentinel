from graphql.language.visitor import Visitor, visit
from graphql.language.ast import DocumentNode

SENSITIVE_KEYWORDS = ["password", "email", "creditCard", "ssn", "token", "secret"]
INTROSPECTION_FIELDS = ["__schema", "__type", "__typename"]

class SemanticVisitor(Visitor):
    def __init__(self):
        super().__init__()
        self.introspection_score = 0
        self.sensitive_field_count = 0
        self.mutation_score = 0

    def enter_field(self, node, key, parent, path, ancestors):
        field_name = node.name.value
        
        if field_name in INTROSPECTION_FIELDS:
            self.introspection_score += 1
            
        for keyword in SENSITIVE_KEYWORDS:
            if keyword in field_name.lower():
                self.sensitive_field_count += 1
                break

    def enter_operation_definition(self, node, *args):
        if node.operation.value == 'mutation':
            self.mutation_score = 1

def extract_semantic_features(ast: DocumentNode) -> dict:
    visitor = SemanticVisitor()
    visit(ast, visitor)
    
    return {
        "introspection_score": visitor.introspection_score,
        "sensitive_field_count": visitor.sensitive_field_count,
        "mutation_score": visitor.mutation_score
    }
