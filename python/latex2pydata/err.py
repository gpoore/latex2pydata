# -*- coding: utf-8 -*-
#
# Copyright (c) 2023, Geoffrey M. Poore
# All rights reserved.
#
# Licensed under the BSD 3-Clause License:
# http://opensource.org/licenses/BSD-3-Clause
#


class Latex2PydataError(Exception):
    pass

class Latex2PydataInvalidMetadataError(Latex2PydataError):
    pass

class Latex2PydataSchemaError(Latex2PydataInvalidMetadataError):
    pass

class Latex2PydataInvalidDataError(Latex2PydataError):
    pass
