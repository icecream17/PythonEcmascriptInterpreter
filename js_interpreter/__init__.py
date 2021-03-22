"""
An implementation of JS in python, for educational purposes
"""

# This file doesn't implement much of the spec, it's split up.
# Sections (Introduction) to (4.3 ECMAScript Overview) don't need any code.

# (4.4 Terms and Definitions) will soon hopefully be supported by (Terms.py)


import asyncio
import inspect # Only used in isThingClassOrDescriptorClass

import typing
from typing import Union, List

# Importing ...itself?
import js_interpreter
from js_interpreter.errors import SubclassError
from js_interpreter.TypesAndValues import Type


CURRENT_IMPLEMENTATION_PROGRESS: typing.Final = '4.4.3: host-defined'
"""This implementation supports clauses 0 thru CURRENT_IMPLEMENTATION_PROGRESS, inclusive"""


######################################
#     Extremely Abstract Classes     #
######################################

descriptors = {} # See ```Descriptor```. Maps descriptor names to descriptors

described_by = []
""""described_by" is an attribute on values where js_interpreter.isThing(value) == True

Here, this is only for describing the js_interpreter itself.
For example, the js_interpreter is described by Descriptor("unfinished non-conforming implementation")
"""

defined_at: typing.Final = None
"""defined_at will always be None"""

class Thing:
   """Creates a... thing"""

   described_by = []
   defined_at = None

   def __init__(self, name=None, definedAt=None):
      self.described_by = []
      self.defined_at: Union[None, DefinitionLocation, List[DefinitionLocation]] = None

      if name is not None:
         self.name = name
      if definedAt is not None:
         self.addDefinitionLocation(definedAt)

      if issubclass(self.__class__, Type):
         self.type = self.__class__
         self.has = {}

   def addDescriptor(self, descriptorName: str):
      try:
         Descriptor(descriptorName).describe(self)
      except ValueError:
         descriptors[descriptorName].describe(self)

   def isDescribedBy(self, textOrDescriptor):
      checked = []
      to_check = self.described_by[:]
      for adjective in to_check:
         if adjective in checked:
            continue

         if adjective is textOrDescriptor:
            return True
         elif adjective.name == textOrDescriptor:
            return True
         
         checked.append(adjective)
         to_check += adjective._is_also
         to_check += adjective._parents
         
      return False

   def addDefinitionLocation(self, location, loose=False):
      """
      Marks where something is defined in the specification.
      """
      locationDescriptor = getDefinitionLocationAndCreateIfUndefined(location)
      locationDescriptor.describe(self, loose=loose)


class Descriptor (Thing):
   """
   | Aka: Adjective.
   |
   | This class describes a Thing.
   | A Descriptor is also a Thing, which means that Descriptors can describe otherDescriptors.
   """

   described_by = []
   defined_at = None

   # Where isFinite is a boolean for whether the set of things it describes is Finite
   def __init__(self, name: str, parents=None, synonyms=None, isFinite=False, __doc__=None):
      global descriptors
      if name in descriptors:
         raise ValueError('Descriptor with this name already exists')

      if parents is None:
         parents = []
      if synonyms is None:
         synonyms = []

      try:
         self._parents = [descriptors[parent_name] for parent_name in parents]
      except KeyError as error:
         raise KeyError("Has parents that don't exist") from error


      self._is_also = []
      for synonym in synonyms:
         if isDescriptor(synonym):
            self._is_also.append(synonym)
         else:
            try:
               self._is_also.append(descriptors[synonym])
            except KeyError:
               self._is_also.append(type(self)(synonym))

      for equivalent in self._is_also:
         if self not in equivalent._is_also:
            equivalent._is_also.append(self)
      

      self.__doc__ = 'Descriptor: ' + name
      if __doc__ is not None:
         self.__doc__ += '\n\n' + __doc__


      if isFinite:
         self.values = []


      super().__init__(name=name)
      descriptors[name] = self

   def __str__(self):
      return self.name

   def __repr__(self):
      return '<Descriptor> ' + self.name

   def describe(self, value: Thing, loose=False):
      """
      Use this to describe a Thing
      
      If you're not describing a Thing, but (value.defined_at.append) exists,
      and you're really sure about this, you can pass <loose=False>
      """

      if not isThing(value) and not loose:
         raise TypeError(
            "The module js_interpreter has an extremely abstract class called Thing.\n"
            "Your value is not an instance of Thing.\n"
            "If you want to ignore this, set the named argument 'loose' to True")

      try:
         if self not in value.described_by:
            value.described_by.append(self)
      except AttributeError as error:
         raise AttributeError(
            "This wouldn't be a problem if you passed in an instance of Thing. Hmmph\n"
            "Oh well. <value.described_by.append(self) failed>"
         ) from error

      if hasattr(self, 'values'):
         self.values.append(value)

   def describes(self, value):
      """Checks if self describes a value"""
      if self in value.described_by:
         return True
      else:
         try:
            return self._describes(value)
         except AttributeError:
            try:
               return value in self.values
            except AttributeError:
               return False


class ThingClass (type, Descriptor):
   """
   | A metaclass for Thing classes.
   |
   | If you want to create another metaclass, just subclass this.
   | If you want to create a Thing class, metaclass this.
   | If you just want to create a Thing use <js_interpreter.Thing> instead
   """

   described_by = []
   defined_at = None

   def __init__(self, _name, _bases, _dict):
      if not issubclass(self, Thing):
         raise SubclassError("Your new class has to be a subclass of Thing {if metaclass=ThingClass}")
      self.described_by = []
      self.defined_at = None
      self.name = self.__name__
      self.addDefinitionLocation = ThingClass.addDefinitionLocation

   @classmethod
   def addDefinitionLocation(cls, location, loose=False):
      """Marks where something is defined in the specification."""
      locationDescriptor = getDefinitionLocationAndCreateIfUndefined(location)
      locationDescriptor.describe(cls, loose=loose)


class DescriptorClass (ThingClass):
   """
   | This is a metaclass for adjective classes.
   |
   | If you want to create another metaclass, just subclass this.
   | If you want to create a Thing class, metaclass this.
   | If you just want to create an adjective use <js_interpreter.Descriptor> instead
   """

   def __init__(self, _name, _bases, _dict):
      super().__init__(_name, _bases, _dict)
      if not issubclass(self, Descriptor):
         raise SubclassError("Your new class has to be a subclass of Descriptor {if metaclass=DescriptorClass}")


def isThingClassOrDescriptorClass(value: any) -> bool:
   """
   Use this if you want to determine if the value passed in is
   a. the class Thing
   b. the class Descriptor
   c. a subclass of ThingClass 
   d. a subclass of DescriptorClass (already checked because DescriptorClass is a subclass of ThingClass)
   """
   return (
      (value is Thing) or
      (value is Descriptor) or
      (inspect.isclass(value) and issubclass(value, ThingClass))
   )


def isThing (value: any) -> bool:
   """Use this if you want to determine if something is a Thing"""
   if isinstance(value, Thing):
      return True
   if isThingClassOrDescriptorClass(value):
      return True
   if value == js_interpreter:
      return True
   else:
      return False


def isDescriptor(value: any) -> bool:
   """Use this if you want to determine if something is a Descriptor"""
   if isinstance(value, Descriptor):
      return True
   if isThingClassOrDescriptorClass(value):
      return True
   else:
      return False


def getDescriptorAndCreateIfUndefined(descriptorText):
   try:
      return Descriptor(descriptorText)
   except ValueError:
      return descriptors[descriptorText]


def addDefinitionLocationTo(value: Thing, location, loose=False):
   """Marks where something is defined in the specification."""
   locationDescriptor = getDefinitionLocationAndCreateIfUndefined(location)
   locationDescriptor.describe(value, loose=loose)




#######################################################
#  To describe where something is defined in the spec #
#######################################################


specificationLocations = []
specificationLocationDescriptors = {}


class DefinitionLocation (Descriptor, metaclass=DescriptorClass):
   prefix = "Spec definition @ "

   def __init__(self, location: str):
      location = location.strip()
      if ': ' not in location:
         raise ValueError('You must also put the name of the header. Like this: "4.4: Terms and Definitions"')

      super().__init__(name=location)
      self.__doc__ = self.__repr__()
      specificationLocations.append(self)

   def __str__(self):
      return self.name

   def __repr__(self):
      return DefinitionLocation.prefix + self.name

   def describe(self, value: Thing, loose=False):
      """
      Use <js_interpreter.describeDefinitionLocation> instead
      """
      super().describe(value, loose=loose)

      if value.defined_at is None:
         value.defined_at = self
      elif isinstance(value.defined_at, DefinitionLocation):
         value.defined_at = [value.defined_at, self]
      else:
         value.defined_at.append(self)


def getDefinitionLocationAndCreateIfUndefined (location: str):
   """Gets the Definition Location Descriptor corresponding to a location string (AndCreateIfUndefined)"""
   if location in specificationLocations:
      return specificationLocationDescriptors[location]
   else:
      specificationLocationDescriptors[location] = DefinitionLocation(location)
      return specificationLocationDescriptors[location]


def createDescriptorWithDefinitionLocation (descriptorText: str, location: str, **kwargs):
   """Creates a Descriptor described by a Definition Location"""
   localDescriptor = Descriptor(descriptorText, **kwargs)
   localDescriptor.addDefinitionLocation(location)
   return localDescriptor


# Adding a descriptor to this Implementation itself
createDescriptorWithDefinitionLocation('implementation (non-conforming)', '4.2: Hosts and Implementations').describe(js_interpreter)



######################################
#              Finally               #
######################################


async def parse():
   """Unimplemented parser function"""
   raise NotImplementedError("Parsing is not implemented yet. Current progress is: " + CURRENT_IMPLEMENTATION_PROGRESS)


async def run():
   """Unimplemented runner function"""
   raise NotImplementedError("I haven't even implemented parsing yet... Current progress is: " + CURRENT_IMPLEMENTATION_PROGRESS)
