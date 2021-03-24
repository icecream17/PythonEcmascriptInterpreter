import typing
from js_interpreter import Thing


class Unique (Thing):
   def __init__(self, description):
      self.description = description
   
   def __str__(self):
      return f"Unique({self.description})"

   def __repr__(self):
      return self.__str__()