"""GraphQLDateTime type"""

from datetime import datetime
from typing import Any, Optional

from graphql.error import GraphQLError
from graphql.language import StringValueNode, ValueNode, print_ast
from graphql.type.definition import GraphQLScalarType
from graphql.pyutils import inspect

from jetblack_iso8601 import iso8601_to_datetime


def _serialize_datetime(output_value: Any) -> datetime:
    if isinstance(output_value, datetime):
        return output_value

    try:
        if isinstance(output_value, str):
            value = iso8601_to_datetime(output_value)
            if value is not None:
                return value
        raise ValueError("Invalid datetime")
    except ValueError as error:
        raise GraphQLError(
            "DateTime cannot represent value: " + inspect(output_value)
        ) from error


def _coerce_datetime(input_value: Any) -> datetime:
    if isinstance(input_value, datetime):
        return input_value

    try:
        if isinstance(input_value, str):
            value = iso8601_to_datetime(input_value)
            if value is not None:
                return value
        raise ValueError('Unable to parse datetime')
    except ValueError as error:
        raise GraphQLError(
            "DateTime cannot represent value: " + inspect(input_value)
        ) from error


def _parse_datetime_literal(
        value_node: ValueNode,
        _variables: Optional[Any] = None
) -> datetime:
    if not isinstance(value_node, StringValueNode):
        raise GraphQLError(
            "DateTime cannot represent non-string value: " +
            print_ast(value_node)
        )
    value = iso8601_to_datetime(value_node.value)
    if value is not None:
        return value

    raise GraphQLError(
        "DateTime cannot represent  value: " +
        print_ast(value_node)
    )


GraphQLDateTime = GraphQLScalarType(
    name="DateTime",
    description="The `DateTime` type represents ISO 8601 datetimes",
    serialize=_serialize_datetime,
    parse_value=_coerce_datetime,
    parse_literal=_parse_datetime_literal
)
