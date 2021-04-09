"""
An implementation of JS in python, for educational purposes
"""

import datetime
import typing

import js_interpreter._utils as _utils


CURRENT_IMPLEMENTATION_PROGRESS: typing.Final = '0: Introduction'
"""This implementation supports clauses 0 thru CURRENT_IMPLEMENTATION_PROGRESS, inclusive"""

LAST_ECMA262_COMMIT: typing.Final = _utils.Commit(
   0x26061c0e5e4b62fae91a7127b46c1efa8b94c4b4, datetime.date(2021, 4, 9))
