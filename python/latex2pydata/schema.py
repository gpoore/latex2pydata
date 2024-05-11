# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


from __future__ import annotations

import itertools
import re
from typing import Callable, Type
from .err import Latex2PydataSchemaError
from .util import KeyDefaultDict




annot_scalars: dict[str, Type] = {
    'bool': bool,
    'bytes': bytes,
    'float': float,
    'int': int,
    'None': type(None),
    'str': str,
    'tuple': tuple,
}
annot_sequences: dict[str, Type] = {
    'list': list,
}
annot_sets: dict[str, Type] = {
    'set': set,
}
annot_mappings: dict[str, Type] = {
    'dict': dict,
}
annot_collections: dict[str, Type] = {
    **annot_sequences,
    **annot_sets,
    **annot_mappings,
}
annot_any_single_scalar_pattern = '|'.join(k for k in annot_scalars)
annot_any_scalar_pattern = rf'(?:{annot_any_single_scalar_pattern})(?:\|(?:{annot_any_single_scalar_pattern}))*'
annot_any_sequence_name_pattern = '|'.join(k for k in annot_sequences)
annot_any_sequence_or_set_name_pattern = '|'.join(k for k in itertools.chain(annot_sets, annot_sequences))
annot_any_mapping_name_pattern = '|'.join(k for k in annot_mappings)
annot_any_scalar_collection_pattern = '|'.join([
    rf'(?:{annot_any_sequence_or_set_name_pattern})\[{annot_any_scalar_pattern}\]',
    rf'(?:{annot_any_mapping_name_pattern})\[{annot_any_scalar_pattern},{annot_any_scalar_pattern}\]',
])
annot_any_nested_collection_pattern = '|'.join([
    rf'(?:{annot_any_sequence_name_pattern})\[(?:{annot_any_scalar_collection_pattern})\]',
    rf'(?:{annot_any_mapping_name_pattern})\[{annot_any_scalar_pattern},(?:{annot_any_scalar_collection_pattern})\]',
])
annot_any_pattern = '|'.join([
    annot_any_scalar_pattern,
    annot_any_scalar_collection_pattern,
    annot_any_nested_collection_pattern,
])
annot_re = re.compile(annot_any_pattern)




def validator_factory(annot: str) -> Callable[[str], bool]:
    if '[' not in annot:
        try:
            scalar_types = [annot_scalars[s] for s in annot.split('|')]
        except KeyError:
            raise Latex2PydataSchemaError(f'Invalid or unsupported schema scalar type "{annot}"')
        if len(scalar_types) == 1:
            scalar_type = scalar_types[0]
            return lambda x: isinstance(x, scalar_type)
        scalar_types = tuple(scalar_types)
        return lambda x: any(isinstance(x, t) for t in scalar_types)
    collection_name, collection_arg = annot.split('[', 1)
    try:
        collection_type = annot_collections[collection_name]
    except KeyError:
        raise Latex2PydataSchemaError(f'Invalid or unsupported schema collection type "{collection_name}"')
    if collection_arg.endswith(']'):
        collection_arg = collection_arg[:-1]
    else:
        raise Latex2PydataSchemaError(f'Invalid or unsupported schema type "{annot}"')
    if collection_name not in annot_mappings:
        sub_validate = validator_dict[collection_arg]
        def validate(x):
            if not isinstance(x, collection_type):
                return False
            if not all(sub_validate(x_n) for x_n in x):
                return False
            return True
        return validate
    key_arg, value_arg = collection_arg.split(',', 1)
    key_validate = validator_dict[key_arg]
    value_validate = validator_dict[value_arg]
    def validate(x):
        if not isinstance(x, collection_type):
            return False
        if not all(key_validate(k) and value_validate(v) for k, v in x.items()):
            return False
        return True
    return validate

validator_dict = KeyDefaultDict(validator_factory)
