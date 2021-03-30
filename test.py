"""
This file tests the js_interpreter package
It does some initial simple checks and then does the tests from the test262 repo.

Some examples of simple checks are "does this compile?", "does this function exist?", and "is there any documentation?"

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

# 0
assert True, "This test file has valid syntax!"


# 1
def isStringOrContainer(value):
   return isinstance(value, (str, list, tuple, range, dict, set, frozenset))


assert True, "Test initialization didn't crash!"

# 2
import js_interpreter
assert True, "Importing doesn't crash!"

# 3
assert hasattr(js_interpreter, "CURRENT_IMPLEMENTATION_PROGRESS")

# 4
assert isStringOrContainer(js_interpreter.CURRENT_IMPLEMENTATION_PROGRESS)

# 5
assert hasattr(js_interpreter, "LAST_ECMA262_COMMIT")

# 6
assert isStringOrContainer(js_interpreter.LAST_ECMA262_COMMIT)
