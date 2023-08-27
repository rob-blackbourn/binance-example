"""GraphQL numeric type

Rather than decide ont eh numeric representation, provide a level of
indirection.
"""

# from graphql import GraphQLString
# GraphQLNumeric = GraphQLString

from .decimal import GraphQLDecimal
GraphQLNumeric = GraphQLDecimal
