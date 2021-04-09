"""
A bunch of simple tests for js_interpreter
"""
# pylint: disable=relative-beyond-top-level, protected-access, no-self-use, missing-function-docstring, missing-class-docstring

import datetime
import inspect

import pytest

from context import interpreter
from context import interpreter_errors
from context import interpreter_unicode
from context import interpreter_utils

_unicode = interpreter_unicode
_utils = interpreter_utils

RangeError = interpreter_errors.RangeError
example_date = datetime.date(2021, 3, 14)


class TestSimple:
   """
   Each class tests a file or subpackage,
   Subclasses can also test functions or classes

   Each class has a bunch of methods,
   which each test some indiviual functionality.

   Each test method has a very descriptive name
   """
   def test_can_start(self):
      assert True, "This file parses!"
      assert True, "Importing didn't crash!"
      assert True, "Test initialization didn't crash!"

   class Test__init__:
      """Tests on the js_interpreter package itself"""

      def test_hasattr_CURRENT_IMPLEMENTATION_PROGRESS(self):
         assert hasattr(interpreter, "CURRENT_IMPLEMENTATION_PROGRESS")

      def test_attr_CURRENT_IMPLEMENTATION_PROGRESS_is_not_None(self):
         assert interpreter.CURRENT_IMPLEMENTATION_PROGRESS is not None

      def test_hasattr_LAST_ECMA262_COMMIT(self):
         assert hasattr(interpreter, "LAST_ECMA262_COMMIT")

      def test_attr_LAST_ECMA262_COMMIT__class__is_Commit(self):
         assert interpreter.LAST_ECMA262_COMMIT.__class__ is _utils.Commit

   class Test_unicode:
      def test_exists(self):
         assert hasattr(interpreter, "_unicode")

   class Test_utils:
      def test_exists(self):
         assert hasattr(interpreter, "_utils")

      def test_hasattr_Commit(self):
         assert hasattr(_utils, "Commit")

      def test_attr_Commit_is_a_class(self):
         assert inspect.isclass(_utils.Commit)

      class Test_utils_Commit:
         def test_Errors_if_commit_id_is_not_an_integer(self):
            with pytest.raises(RangeError):
               _utils.Commit(0.5, example_date)

         def test_Errors_if_commit_id_is_negative(self):
            with pytest.raises(RangeError):
               _utils.Commit(-1, example_date)

         def test_Errors_if_commit_id_is_too_big(self):
            with pytest.raises(RangeError):
               _utils.Commit(2 ** 160, example_date)
