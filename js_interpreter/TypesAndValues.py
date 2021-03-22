from js_interpreter import Thing, ThingClass
from js_interpreter.errors import SubclassError
from js_interpreter._unique import Unique

######################################
#                Type                #
######################################

class Type (ThingClass):
   values = []

   def __init__(self, _name, _bases, _dict):
      super().__init__(_name, _bases, _dict)

      if not hasattr(self, 'has'):
         raise AttributeError("Your new type must have the attribute <has>")

      self._describes = Type._describes

   @classmethod
   def _describes(cls, value: Thing):
      return isinstance(value, cls)


class LanguageType (Type):
   values = []

   def __init__(self, _name, _bases, _dict):
      super().__init__(_name, _bases, _dict)


class PrimitiveType (LanguageType):
   values = []

   def __init__(self, _name, _bases, _dict):
      super().__init__(_name, _bases, _dict)
      # TODO: Add primitive value descriptor


undefined_value = Unique('undefined')

class UndefinedType (PrimitiveType):
   values = (undefined_value,)

   def __init__(self, _name, _bases, _dict):
      super().__init__(_name, _bases, _dict)

   def __new__(self, *_args):
      return undefined_value


