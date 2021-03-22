import typing
from blessings import Terminal
Style = Terminal

class Unique:
   def __init__(self, description):
      self.description = description
   
   def __str__(self):
      return f"Unique({self.description})"

   def __repr__(self):
      return self.__str__()

   def print(self):
      print(f"{Style.dim}Unique({Style.normal}{Style.bold}{self.description}{Style.normal}{Style.dim}){Style.normal}")