# "A directory containing a __init__.py is identified as a package"

import asyncio
import typing
from typing import Final
import unicodedata


# Importing ...itself?
from js_interpreter import _unicode


CURRENT_IMPLEMENTATION_PROGRESS: Final = '0 - Introduction'


######################################
#     Extremely Abstract Classes     #
######################################

class Thing:
   pass


class Descriptor (Thing):
   def __init__(self, name: str):
      self.name = name
      descriptors.append(self)

   def __str__(self):
      return self.name


descriptors = []


def isThingClassOrDescriptorClass (value: any) -> bool:
   return (value is Thing) or (value is Descriptor)


def isThing (value: any) -> bool:
   if isinstance(value, Thing):
      return True
   if isThingClassOrDescriptorClass(value):
      return True
   else:
      return False


def isDescriptor (value) -> bool:
   if isinstance(value, Descriptor):
      return True
   if isThingClassOrDescriptorClass(value):
      return True
   else:
      return False





######################################
#              Finally               #
######################################


async def parse():
   raise NotImplementedError("Parsing is not implemented yet. Current progress is: " + CURRENT_IMPLEMENTATION_PROGRESS)


async def run():
   raise NotImplementedError("I haven't even implemented parsing yet... Current progress is: " + CURRENT_IMPLEMENTATION_PROGRESS)
