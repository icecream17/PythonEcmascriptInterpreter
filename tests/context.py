"""
A file that modifies the path so that js_interpreter can be imported

Stolen from and recommended by
https://docs.python-guide.org/writing/structure/

python-guide is copyrighted,
   ©2011-2021 Kenneth Reitz & Real Python
   See https://docs.python-guide.org/notes/license/

   CC BY-NC-SA 3.0
   https://creativecommons.org/licenses/by-nc-sa/3.0/

Changes:
1. Docstring + Pylint ignore comment + Newline at start of file
2. Newline after `import sys`
3. `sample` changed to `js_interpreter`
4. Newline at end of file
"""
# pylint: disable=import-error, wrong-import-position, unused-import

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import js_interpreter as interpreter
import js_interpreter.errors as interpreter_errors
import js_interpreter._storage as interpreter_storage
import js_interpreter._unicode as interpreter_unicode
import js_interpreter._utils as interpreter_utils
