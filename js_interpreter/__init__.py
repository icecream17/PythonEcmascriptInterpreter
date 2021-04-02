"""
An implementation of JS in python, for educational purposes
"""

import datetime
import typing

import js_interpreter._utils as _utils


CURRENT_IMPLEMENTATION_PROGRESS: typing.Final = '0: Introduction'
"""This implementation supports clauses 0 thru CURRENT_IMPLEMENTATION_PROGRESS, inclusive"""

LAST_ECMA262_COMMIT: typing.Final = _utils.Commit(
   0xa12b4d4420adddb660ecd3e81f3ef737b1b100d8, datetime.date(2021, 4, 1))
