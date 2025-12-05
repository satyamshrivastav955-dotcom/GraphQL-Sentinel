from graphql.language.visitor import Visitor, visit
from graphql.language.ast import DocumentNode

class DepthVisitor(Visitor):
    def __init__(self):
        self.max_depth = 0
        self.current_depth = 0

    def enter_field(self, node, key, parent, path, ancestors):
        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)

    def leave_field(self, node, key, parent, path, ancestors):
        self.current_depth -= 1

def get_query_depth(ast: DocumentNode) -> int:
    visitor = DepthVisitor()
    visit(ast, visitor)
    return visitor.max_depth

def get_operation_type(ast: DocumentNode) -> str:
    for definition in ast.definitions:
        if hasattr(definition, 'operation'):
            return definition.operation.value
    return "query"
