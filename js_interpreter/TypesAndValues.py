from js_interpreter import Thing, ThingClass
from js_interpreter.errors import SubclassError, FiniteCreationError
from js_interpreter._unique import Unique

######################################
#            Type & Value            #
######################################

# Wait, what creates the values?

# "Algorithms within this specification manipulate values each of which has an associated type."
# Value classes create values which are thereafter associated with their types



# The below classes create Types / ValueClasses


class TypeCreatorMeta (ThingClass):
   def __init__(self, _name, _bases, _dict):
      super().__init__(_name, _bases, _dict)


class ValueMetaClass (ThingClass):
   def __init__(self, _name, _bases, _dict):
      super().__init__(_name, _bases, _dict)

      if not hasattr(self, 'associatedType'):
         raise AttributeError('Value class must have an associated type')
      if not isinstance(type(self.associatedType), TypeCreatorMeta):
         raise TypeError('Metaclass must be isinstance TypeCreatorMeta')


class LanguageType (Thing, metaclass=TypeCreatorMeta):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)


class LanguageValue (ValueMetaClass):
   def __init__(self, _name, _bases, _dict):
      super().__init__(_name, _bases, _dict)

      if not isinstance(type(self.associatedType), TypeCreatorMeta):
         raise TypeError('Metaclass must be isinstance LanguageType')


####################################################################################
def _createAllFiniteValues(ValueClass, valueNameList):
   for name in valueNameList:
      ValueClass(name)


undefined = None

class UndefinedType:
   def __init__(self):
      raise Exception('Use the other class')

class UndefinedValue (Thing, metaclass=LanguageValue):
   _creationCount = 0

   def __init__(self):
      global undefined
      undefined = self
      self.has = {}

   def __new__(self, *args, **kwargs):
      if UndefinedValue._creationCount == 0:
         return super().__new__(*args, **kwargs)
      else:
         return undefined

UndefinedValue()


