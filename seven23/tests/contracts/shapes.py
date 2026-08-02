"""Recursive JSON shape assertions for API contract tests."""

from __future__ import annotations

from typing import Any


class Optional:
    """Wrap a type/schema so the key may be absent (but not null unless type allows)."""

    def __init__(self, schema: Any):
        self.schema = schema


class Nullable:
    """Value may be null or match the wrapped schema."""

    def __init__(self, schema: Any):
        self.schema = schema


class AnyOf:
    """Value must match at least one of the given schemas."""

    def __init__(self, *schemas: Any):
        self.schemas = schemas


class ListOf:
    """Homogeneous list; each item must match ``item_schema``."""

    def __init__(self, item_schema: Any, *, allow_empty: bool = True):
        self.item_schema = item_schema
        self.allow_empty = allow_empty


class DictOf:
    """Object with unknown keys whose values match ``value_schema``."""

    def __init__(self, value_schema: Any):
        self.value_schema = value_schema


def assert_json_shape(data: Any, schema: Any, path: str = '$') -> None:
    """
    Assert ``data`` matches ``schema``.

    Schema forms:
      - ``dict``: object with exact required keys; use ``Optional(x)`` for optional keys
      - ``ListOf(item)`` or ``[item]``: list of items
      - ``Nullable(x)``: null or x
      - ``AnyOf(a, b)``: union
      - ``DictOf(v)``: map of string keys to values
      - builtin types (``str``, ``int``, ``bool``, ``float``): isinstance check
      - ``True``: any JSON value accepted
    """
    if isinstance(schema, Optional):
        raise AssertionError(
            f'{path}: Optional() is only valid as a dict value marker, not a root schema'
        )

    if schema is True:
        return

    if isinstance(schema, Nullable):
        if data is None:
            return
        assert_json_shape(data, schema.schema, path)
        return

    if isinstance(schema, AnyOf):
        errors = []
        for candidate in schema.schemas:
            try:
                assert_json_shape(data, candidate, path)
                return
            except AssertionError as exc:
                errors.append(str(exc))
        raise AssertionError(
            f'{path}: value {data!r} matched none of {len(schema.schemas)} alternatives:\n'
            + '\n'.join(f'  - {e}' for e in errors)
        )

    if isinstance(schema, DictOf):
        if not isinstance(data, dict):
            raise AssertionError(f'{path}: expected object, got {type(data).__name__}: {data!r}')
        for key, value in data.items():
            assert_json_shape(value, schema.value_schema, f'{path}.{key}')
        return

    if isinstance(schema, ListOf) or (
        isinstance(schema, list) and len(schema) == 1
    ):
        item_schema = schema.item_schema if isinstance(schema, ListOf) else schema[0]
        allow_empty = schema.allow_empty if isinstance(schema, ListOf) else True
        if not isinstance(data, list):
            raise AssertionError(f'{path}: expected array, got {type(data).__name__}: {data!r}')
        if not allow_empty and not data:
            raise AssertionError(f'{path}: expected non-empty array')
        for index, item in enumerate(data):
            assert_json_shape(item, item_schema, f'{path}[{index}]')
        return

    if isinstance(schema, dict):
        if not isinstance(data, dict):
            raise AssertionError(f'{path}: expected object, got {type(data).__name__}: {data!r}')

        required = {}
        optional = {}
        for key, value_schema in schema.items():
            if isinstance(value_schema, Optional):
                optional[key] = value_schema.schema
            else:
                required[key] = value_schema

        missing = [key for key in required if key not in data]
        if missing:
            raise AssertionError(f'{path}: missing keys {missing}; got keys {sorted(data)}')

        allowed = set(required) | set(optional)
        unexpected = sorted(set(data) - allowed)
        if unexpected:
            raise AssertionError(
                f'{path}: unexpected keys {unexpected}; allowed {sorted(allowed)}'
            )

        for key, value_schema in required.items():
            assert_json_shape(data[key], value_schema, f'{path}.{key}')
        for key, value_schema in optional.items():
            if key in data:
                assert_json_shape(data[key], value_schema, f'{path}.{key}')
        return

    if schema is int:
        # bool is a subclass of int in Python — reject booleans explicitly.
        if type(data) is not int:
            raise AssertionError(f'{path}: expected int, got {type(data).__name__}: {data!r}')
        return

    if schema in (str, bool, float, list, dict):
        if not isinstance(data, schema):
            raise AssertionError(
                f'{path}: expected {schema.__name__}, got {type(data).__name__}: {data!r}'
            )
        return

    raise AssertionError(f'{path}: unsupported schema {schema!r}')
