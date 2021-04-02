"""
This file tests the js_interpreter package
It does some initial simple checks and then does the tests from the test262 repo.

Some examples of simple checks are "does this compile?", "does this function exist?",
and "is there any documentation?"

Each simple check has an index

Then there are the test262 tests.
I'll create another package, and i'll do something like this:

```python
import myOwnTest262
myOwnTest262.run_tests(
   createNewRealm = someFunction,
   evaluateText = takesRealmAndTextAndDoesSomething,
   exceptionDirection = someError.Thing,
)
```
"""

import datetime
import pytest

import js_interpreter
import js_interpreter._utils as _utils


def test_simple___init__():
   """
   Runs simple checks for the __init__ file of js_interpreter
   """
   # 0
   assert True, "This test file has valid syntax and importing didn't crash!"

   # 1
   # In the future there's will be more stuff here
   assert True, "Test initialization didn't crash!"

   # 2
   assert hasattr(js_interpreter, "CURRENT_IMPLEMENTATION_PROGRESS")

   # 3
   assert js_interpreter.CURRENT_IMPLEMENTATION_PROGRESS is not None

   # 4
   assert hasattr(js_interpreter, "LAST_ECMA262_COMMIT")

   # 5
   assert js_interpreter.LAST_ECMA262_COMMIT.__class__ is _utils.Commit


def test_simple__unicode():
   """
   Runs simple checks for the _unicode file of js_interpreter
   """
   # TODO


def test_simple__utils__init__():
   """
   Runs simple checks for the __init__ file of js_interpreter._utils
   """
   example_date = datetime.date(2021, 3, 14)

   # _utils.Commit
   # 0
   with pytest.raises(AssertionError):
      _utils.Commit(0.5, example_date)

   # 1
   with pytest.raises(AssertionError):
      _utils.Commit(-1, example_date)

   # 2
   with pytest.raises(AssertionError):
      _utils.Commit(2 ** 160, example_date)
