"""GraphQL decimal type"""

from decimal import Decimal, InvalidOperation
from typing import Any, Optional

from graphql.error import GraphQLError
from graphql.language import StringValueNode, IntValueNode, ValueNode, print_ast
from graphql.type.definition import GraphQLScalarType
from graphql.pyutils import inspect


def _serialize_decimal(output_value: Any) -> Decimal:
    if isinstance(output_value, Decimal):
        return output_value

    try:
        if isinstance(output_value, str):
            return Decimal(output_value)
        elif isinstance(output_value, int):
            return Decimal(output_value)
        raise ValueError("invalid decimal")
    except ValueError as error:
        raise GraphQLError(
            "Decimal cannot represent value: " + inspect(output_value)
        ) from error


def _coerce_decimal(input_value: Any) -> Decimal:
    if isinstance(input_value, Decimal):
        return input_value

    try:
        if isinstance(input_value, str):
            return Decimal(input_value)
        elif isinstance(input_value, int):
            return Decimal(input_value)
        raise ValueError("unable to parse decimal")
    except ValueError as error:
        raise GraphQLError(
            "Decimal cannot represent value: " + inspect(input_value)
        ) from error


def _parse_decimal_literal(
        value_node: ValueNode,
        _variables: Optional[Any] = None
) -> Decimal:
    if not isinstance(value_node, (StringValueNode, IntValueNode)):
        raise GraphQLError(
            "Decimal cannot represent non string value: " +
            print_ast(value_node)
        )

    try:
        return Decimal(value_node.value)
    except InvalidOperation as error:
        raise GraphQLError(
            "Decimal cannot represent value: " + print_ast(value_node)
        ) from error


GraphQLDecimal = GraphQLScalarType(
    name="Decimal",
    description="The 'Decimal' type represents decimals",
    serialize=_serialize_decimal,
    parse_value=_coerce_decimal,
    parse_literal=_parse_decimal_literal
)
