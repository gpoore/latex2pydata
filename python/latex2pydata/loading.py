# -*- coding: utf-8 -*-
#
# Copyright (c) 2023-2024, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# https://opensource.org/license/BSD-3-Clause
#


from __future__ import annotations

import ast
import io
import pathlib
import re
from typing import Any, Literal
from .err import Latex2PydataInvalidMetadataError, Latex2PydataSchemaError, Latex2PydataInvalidDataError
from .schema import annot_re, validator_dict




metadata_comment_pattern = '# latex2pydata metadata:'

key_pattern = r'[A-Za-z_][0-9A-Za-z_]*'
keypath_pattern = rf'{key_pattern}(?:\.{key_pattern})*'
keypath_re = re.compile(keypath_pattern)




def load(readable: pathlib.Path | io.BytesIO | io.TextIOBase,
         encoding: str | None = None,
         schema: dict[str, str] | None = None,
         schema_missing: Literal['error'] | Literal['verbatim'] | Literal['evalany'] | None = None) -> dict[str, Any] | list[dict[str, Any]]:
    if isinstance(readable, pathlib.Path):
        encoding = encoding or 'utf-8-sig'
        return loads(readable.read_text(encoding=encoding), schema, schema_missing)
    raw_read: bytes | str = readable.read()
    if isinstance(raw_read, bytes):
        encoding = encoding or 'utf-8-sig'
        return loads(raw_read.decode(encoding), schema, schema_missing)
    if isinstance(raw_read, str):
        if encoding is not None:
            raise TypeError(f'Cannot specify encoding "{encoding}" for a readable that returns a string')
        return loads(raw_read, schema, schema_missing)
    raise TypeError


def loads(string: str,
          schema: dict[str, str] | None = None,
          schema_missing: Literal['error'] | Literal['verbatim'] | Literal['evalany'] | None = None) -> dict[str, Any] | list[dict[str, Any]]:

    if string.startswith(metadata_comment_pattern):
        metadata_str = string[len(metadata_comment_pattern):string.find('\n')].strip()
        try:
            metadata = ast.literal_eval(metadata_str)
        except Exception as e:
            raise Latex2PydataInvalidMetadataError(f'Loading metadata failed:\n{e}')
        if not isinstance(metadata, dict):
            raise Latex2PydataInvalidMetadataError('Invalid metadata (must be a dict)')
        if schema is None and 'schema' in metadata:
            schema = metadata['schema']
        if schema_missing is None and 'schema_missing' in metadata:
            schema_missing = metadata['schema_missing']
    if schema is not None:
        if not isinstance(schema, dict):
            raise Latex2PydataSchemaError('Invalid schema (must be dict[str, str])')
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in schema.items()):
            raise Latex2PydataSchemaError('Invalid schema (must be dict[str, str])')
        schema = {k: v.replace(' ', '') for k, v in schema.items()}
        for k, v in schema.items():
            if not keypath_re.fullmatch(k):
                raise Latex2PydataSchemaError(f'Invalid or unsupported schema key "{k}"')
            if v != 'verbatim' and not annot_re.fullmatch(v):
                raise Latex2PydataSchemaError(
                    f'Invalid or unsupported schema value (type annotation) "{v}"'
                )
    if schema_missing == 'rawstr':
        # Backward compatibility for < v0.5.0
        schema_missing = 'verbatim'
    if schema_missing is None:
        schema_missing = 'error'
    elif schema_missing not in ('error', 'verbatim', 'evalany'):
        raise Latex2PydataInvalidMetadataError(f'Invalid "schema_missing" value "{schema_missing}"')

    try:
        raw_data: dict[str, str] | list[dict[str, str]] = ast.literal_eval(string)
    except Exception as e:
        raise Latex2PydataInvalidDataError(f'Loading data with ast.literal_eval() failed:\n{e}')
    top_is_list: bool
    if isinstance(raw_data, list):
        top_is_list = True
        raw_data_list = raw_data
    elif isinstance(raw_data, dict):
        top_is_list = False
        raw_data_list = [raw_data]
    else:
        raise Latex2PydataInvalidDataError(
            'Before any schema is applied, data must be dict[str, str] or list[dict[str, str]]'
        )
    for obj in raw_data_list:
        if not isinstance(obj, dict):
            raise Latex2PydataInvalidDataError(
                'Before any schema is applied, data must be dict[str, str] or list[dict[str, str]]'
            )
        for k, v in obj.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise Latex2PydataInvalidDataError(
                    'Before any schema is applied, data must be dict[str, str] or list[dict[str, str]]'
                )
            if not keypath_re.fullmatch(k):
                raise Latex2PydataInvalidDataError(f'Unsupported key name "{k}"')

    data = []
    for raw_data_dict in raw_data_list:
        data_dict = {}
        data.append(data_dict)
        for raw_k, raw_v in raw_data_dict.items():
            if schema is None:
                v = raw_v
            elif raw_k in schema:
                value_type_annot = schema[raw_k]
                if value_type_annot == 'verbatim':
                    v = raw_v
                else:
                    try:
                        v = ast.literal_eval(raw_v)
                    except Exception as e:
                        raise Latex2PydataInvalidDataError(f'Invalid value for key "{raw_k}":\n{e}')
                    if not validator_dict[value_type_annot](v):
                        raise Latex2PydataInvalidDataError(f'Key "{raw_k}" should have value with type "{value_type_annot}"')
            elif schema_missing == 'error':
                raise Latex2PydataInvalidDataError(f'Key "{raw_k}" is missing a schema entry')
            elif schema_missing == 'verbatim':
                v = raw_v
            elif schema_missing == 'evalany':
                try:
                    v = ast.literal_eval(raw_v)
                except Exception as e:
                    raise Latex2PydataInvalidDataError(f'Invalid value for key "{raw_k}":\n{e}')
            else:
                raise ValueError
            if '.' not in raw_k:
                data_dict[raw_k] = v
                continue
            keypath = raw_k.split('.')
            loc = data_dict
            for kp_elem in keypath[:-1]:
                try:
                    loc = loc[kp_elem]
                except KeyError:
                    new_dict = {}
                    loc[kp_elem] = new_dict
                    loc = new_dict
            loc[keypath[-1]] = v

    if not top_is_list:
        data = data.pop()

    return data
