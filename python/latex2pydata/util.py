# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


from __future__ import annotations

import collections
from typing import Any, Callable


class KeyDefaultDict(collections.defaultdict):
    '''
    Default dict that passes missing keys to the factory function, rather than
    calling the factory function with no collection_arguments.
    '''
    __init__: Callable[[Callable[[Any], Any]], None]
    default_factory: Callable[[Any], Any]
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = self.default_factory(key)
        return self[key]
