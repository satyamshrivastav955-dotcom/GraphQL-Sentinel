from graphql.language.visitor import Visitor, visit
from graphql.language.ast import DocumentNode

class StructuralVisitor(Visitor):
    def __init__(self):
        super().__init__()
        self.field_count = 0
        self.max_depth = 0
        self.current_depth = 0
        self.alias_count = 0
        self.fragment_count = 0
        self.directive_count = 0

    def enter_field(self, node, key, parent, path, ancestors):
        self.field_count += 1
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)
        if node.alias:
            self.alias_count += 1

    def leave_field(self, node, key, parent, path, ancestors):
        self.current_depth -= 1

    def enter_fragment_definition(self, node, *args):
        self.fragment_count += 1

    def enter_directive(self, node, *args):
        self.directive_count += 1

def extract_structural_features(ast: DocumentNode) -> dict:
    visitor = StructuralVisitor()
    visit(ast, visitor)
    
    return {
        "field_count": visitor.field_count,
        "max_depth": visitor.max_depth,
        "alias_count": visitor.alias_count,
        "fragment_count": visitor.fragment_count,
        "directive_count": visitor.directive_count
    }
