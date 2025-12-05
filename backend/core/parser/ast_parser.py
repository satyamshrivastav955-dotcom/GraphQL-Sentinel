from graphql import parse, Source, GraphQLError
from graphql.language.ast import DocumentNode
import logging

logger = logging.getLogger(__name__)

class ASTParser:
    @staticmethod
    def parse_query(query: str) -> DocumentNode:
        """
        Parses a GraphQL query string into an AST.
        Returns None if parsing fails.
        """
        try:
            source = Source(query)
            ast = parse(source)
            return ast
        except GraphQLError as e:
            logger.error(f"GraphQL Parse Error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected Error during parsing: {str(e)}")
            return None

    @staticmethod
    def is_valid(query: str) -> bool:
        return ASTParser.parse_query(query) is not None
