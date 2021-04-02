"""
Utils for the js_interpreter package
"""
import typing
import datetime

class Commit:
   """
   Represents a git commit
   """
   def __init__(self, commit_id: int, date: datetime.date):
      assert isinstance(commit_id, int)
      assert commit_id >= 0
      assert commit_id <= 0xffffffffffffffffffffffffffffffffffffffff

      self.id = commit_id
      self.date = date
