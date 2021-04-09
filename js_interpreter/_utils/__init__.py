"""
Utils for the js_interpreter package
"""
import typing
import datetime
from js_interpreter.errors import RangeError

class Commit:
   """Represents a git commit"""
   def __init__(self, commit_id: int, date: datetime.date):
      if not isinstance(commit_id, int):
         raise RangeError(f"commit_id was not an integer: {commit_id}")
      if commit_id < 0:
         raise RangeError(f"commit_id was negative: {commit_id}")
      if commit_id > 0xffffffffffffffffffffffffffffffffffffffff:
         raise RangeError(f"commit_id was too big: {commit_id}")

      self.id = commit_id
      self.date = date
