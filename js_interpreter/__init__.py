"""
An implementation of JS in python, for educational purposes
"""

import asyncio
import typing
import inspect # Only used in isThingClassOrDescriptorClass


# Importing ...itself?
import js_interpreter


CURRENT_IMPLEMENTATION_PROGRESS: typing.Final = '4.4.4: type'
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

defined_at = None
"""defined_at will always be None"""


class Thing:
   """Creates a... thing"""

   described_by = []
   defined_at = None

   def __init__(self, name=None, definedAt=None):
      self.described_by = []
      self.defined_at = None

      if name is not None:
         self.name = name
      if definedAt is not None:
         self.setDefinitionLocation(definedAt)

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

   def setDefinitionLocation(self, location):
      describeDefinitionLocation(self, location) # See global function below


class Descriptor (Thing):
   """
   | Aka: Adjective.
   |
   | This class describes a Thing.
   | A Descriptor is also a Thing, which means that Descriptors can describe otherDescriptors.
   """

   described_by = []
   defined_at = None

   def __init__(self, name: str, parents=[], synonyms=[], __doc__=None):
      global descriptors
      if name in descriptors:
         raise ValueError('Descriptor with this name already exists')

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


class DescriptorClass (type, Descriptor):
   """
   | This is a metaclass for adjective classes.
   |
   | If you just want to create an adjective use <js_interpreter.Descriptor> instead
   """

   described_by = []
   defined_at = None

   def __init__(self, _name, _bases, _dict):
      if not issubclass(self, Thing):
         raise ValueError("Your new class has to be a subclass of Descriptor {if metaclass=DescriptorClass}")
      self.described_by = []
      self.defined_at = None


def isThingClassOrDescriptorClass(value: any) -> bool:
   """Use this if you want to determine the value passed in is
   a. the class Thing
   b. the class Descriptor
   c. a subclass of ThingClass
   c. a subclass of DescriptorClass"""
   return (
      (value is Thing) or
      (value is Descriptor) or
      # TODO: ThingClass
      (inspect.isclass(value) and issubclass(value, DescriptorClass))
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
      value.defined_at = self


def describeDefinitionLocation (value: Thing, location: str, loose=False):
   """Marks where something is defined in the specification."""
   locationDescriptor = getDefinitionLocationAndCreateIfUndefined(location)
   locationDescriptor.describe(value, loose=loose)


def getDefinitionLocationAndCreateIfUndefined (location: str):
   """Gets the Definition Location Descriptor corresponding to a location string (AndCreateIfUndefined)"""
   if location in specificationLocations:
      return specificationLocationDescriptors[location]
   else:
      specificationLocationDescriptors[location] = DefinitionLocation(location)
      return specificationLocationDescriptors[location]


def createDescriptorWithDefinitionLocation (descriptorText: str, location: str, synonyms=[]):
   """Creates a Descriptor described by a Definition Location"""
   localDescriptor = Descriptor(descriptorText, synonyms=synonyms)
   describeDefinitionLocation(localDescriptor, location)
   return localDescriptor


######################################
#             Definitions            #
######################################

# Implementation
createDescriptorWithDefinitionLocation('implementation (non-conforming)', '4.2: Hosts and Implementations').describe(js_interpreter)


# 4.4 Terms and Definitions
def _createTerm(termName, termDefinition, definedAt, synonyms=[]):
   """Used for creating terms defined in section 4.4 of the spec"""
   if ': ' not in definedAt:
      definedAt += ': ' + termName
   
   term = createDescriptorWithDefinitionLocation(termName, definedAt, synonyms=synonyms)
   term.__doc__ += '\n\n' + termDefinition


TermsAndDefinitions = {
   '4.4.1: implementation-approximated': {
      "definition": '"defined in whole or in part by an external source but has a recommended, ideal behaviour"'
   },
   '4.4.2: implementation-defined': {
      "definition": '"defined in whole or in part by an external source"'
   },
   '4.4.3: host-defined': {
      "definition": '"same as implementation-defined;"\n' '"Note: Editorially, see clause 4.2"',
      "synonyms": ['implementation-defined']
   },
   '4.4.4: type': {
      "definition": 
         '"set of data values as defined in clause 6"\n\n'
         'Includes the Language...\n'
         '   Undefined, Null, Boolean, String, Number, BigInt, Object\n'
         '...and Specification types\n'
         '   List, Record, Set, Relation, Completion (Record), Reference Record, Property Descriptor, Environment Record, Abstract Closure, Data Block'
   }
}

for term, termDictionary in TermsAndDefinitions.items():
   definedAt, termName = term.split(': ')
   termDefinition = termDictionary["definition"]
   synonyms = termDictionary["synonyms"] if "synonyms" in termDictionary else []

   _createTerm(termName, termDefinition, definedAt, synonyms=synonyms)

del definedAt
del termName
del termDefinition
del synonyms


######################################
#              Finally               #
######################################


async def parse():
   """Unimplemented parser function"""
   raise NotImplementedError("Parsing is not implemented yet. Current progress is: " + CURRENT_IMPLEMENTATION_PROGRESS)


async def run():
   """Unimplemented runner function"""
   raise NotImplementedError("I haven't even implemented parsing yet... Current progress is: " + CURRENT_IMPLEMENTATION_PROGRESS)
