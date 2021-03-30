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
import js_interpreter
assert True, "Importing doesn't crash!"

# 2
assert hasattr(js_interpreter, "CURRENT_IMPLEMENTATION_PROGRESS")

# 3
assert not (
   isinstance(js_interpreter["CURRENT_IMPLEMENTATION_PROCESS"], type(None)) or
   isinstance(js_interpreter["CURRENT_IMPLEMENTATION_PROCESS"], bool) or
   isinstance(js_interpreter["CURRENT_IMPLEMENTATION_PROCESS"], float) or
   isinstance(js_interpreter["CURRENT_IMPLEMENTATION_PROCESS"], int)
)

# 4
assert hasattr(js_interpreter, "LATEST_ECMA262_COMMIT")

# 5
assert not (
   isinstance(js_interpreter["CURRENT_IMPLEMENTATION_PROCESS"], type(None)) or
   isinstance(js_interpreter["CURRENT_IMPLEMENTATION_PROCESS"], bool) or
   isinstance(js_interpreter["CURRENT_IMPLEMENTATION_PROCESS"], float) or
   isinstance(js_interpreter["CURRENT_IMPLEMENTATION_PROCESS"], int)
)
