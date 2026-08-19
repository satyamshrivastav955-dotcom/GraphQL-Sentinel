"""
GraphQL Query Cost & Complexity Feature Extractor.
Analyzes AST field counts, arguments, and nested pagination multipliers (first/limit/count).
"""
from graphql.language.visitor import Visitor, visit
from graphql.language.ast import DocumentNode, IntValueNode


class CostVisitor(Visitor):
    def __init__(self):
        super().__init__()
        self.complexity = 0
        self.multiplier_stack = [1]
        self.max_multiplier = 1
        self.estimated_cost = 0

    def enter_field(self, node, key, parent, path, ancestors):
        current_multiplier = self.multiplier_stack[-1]
        field_cost = 1
        new_multiplier = 1

        if node.arguments:
            field_cost += len(node.arguments)
            for arg in node.arguments:
                arg_name = arg.name.value.lower()
                if arg_name in ("first", "limit", "count", "size", "last", "take"):
                    if isinstance(arg.value, IntValueNode):
                        try:
                            val = int(arg.value.value)
                            if val > 0:
                                new_multiplier = min(val, 1000)
                        except ValueError:
                            pass

        self.complexity += field_cost
        self.estimated_cost += field_cost * current_multiplier
        next_multiplier = min(current_multiplier * new_multiplier, 100000)
        self.multiplier_stack.append(next_multiplier)
        if next_multiplier > self.max_multiplier:
            self.max_multiplier = next_multiplier

    def leave_field(self, node, key, parent, path, ancestors):
        if len(self.multiplier_stack) > 1:
            self.multiplier_stack.pop()


def extract_cost_features(ast: DocumentNode, query_string: str = "") -> dict:
    """Extract complexity score, pagination multipliers, and token count from GraphQL AST."""
    visitor = CostVisitor()
    visit(ast, visitor)

    token_count = len(query_string.split()) if query_string else 0

    return {
        "complexity_score": visitor.complexity,
        "token_count": token_count,
        "cost_estimate": visitor.estimated_cost,
        "max_multiplier": visitor.max_multiplier,
    }
