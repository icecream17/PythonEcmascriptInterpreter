"""
Package that stores data
Can store data for just 1 session or across sessions
"""
import json
import os.path
import psutil

MAX_MEMORY_USAGE = 75
"""Threshold for memory usage, right now it's 75 percent"""

STORAGE_DIRECTORY = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jsondata')
"""Directory for stored data"""

GLOBAL_STORAGE_DIRECTORY = os.path.join(STORAGE_DIRECTORY, 'global')
SESSION_STORAGE_DIRECTORY = os.path.join(STORAGE_DIRECTORY, 'session')


def get_memory():
   """return psutil.virtual_memory()"""
   return psutil.virtual_memory()


def get_memory_usage():
   """Gets memory usage as a percent, calculated by `(total - available) / toal * 100"""
   return get_memory().percent


def checkMemoryUsage():
   """Checks if more than the threshold percent of memory is being used"""
   if get_memory_usage() > MAX_MEMORY_USAGE:
      print(get_memory())
      raise MemoryError("Using too much memory!")


def createSessionStoragePath(filename):
   return os.path.join(SESSION_STORAGE_DIRECTORY, filename)


def createGlobalStoragePath(filename):
   return os.path.join(GLOBAL_STORAGE_DIRECTORY, filename)


"""
Use `open` to open a file,
and `os.remove` to delete a file
"""
storedItemPaths = set()


def makeUniquePath(dir, is_global=False):
   assert os.path.isdir(dir), "dir argument must be a directory"

   path = dir
   index = 0
   while os.path.join(path, str(index)) in storedItemPaths:
      index += 1

   path = os.path.join(path, str(index))

   if is_global:
      path = createGlobalStoragePath(path)
   else:
      path = createSessionStoragePath(path)

   storedItemPaths.add(path)
   return path


class StoredItem:
   """
   A stored item
   
   Has the following attributes:
   self.object   - The item in question
                   When the item is in storage this property doesn't exist
   self.toData   - Converts the item to data
   self.fromData - Opposite of toData
   self.isStored - Is it stored?
   
   self.path     - getter property
                   The filepath claimed by this StoredItem instance
   """
   def __init__(self, obj, *, dir=None, is_global=False, toData=None, fromData=None):
      """
      obj       - the thing to be stored
      dir       - the dir to store the object at
      is_global - set to True if storing cross-session data
      toData    - callback that converts obj to data
      fromData  - takes the data from toData and converts it back into the object
      """
      assert os.path.isdir(dir), "dir argument must be a directory"
      assert callable(toData), "toData argument must be callable"
      assert callable(fromData), "fromData argument must be callable"
      self.object = obj
      self.toData = toData
      self.fromData = fromData
      self.isStored = False

      self._path = makeUniquePath(dir, is_global=is_global)

   @property
   def path(self):
      """Gets the path of a StoredItem"""
      return self._path

   def store(self):
      if self.isStored:
         raise ValueError("Item is already stored")

      if os.path.exists(self.path):
         raise ValueError("This item isn't stored but the storage file exits!!!!")

      if not hasattr(self, 'object'):
         raise ValueError("This item must've been deleted")

      # Create file
      open(self.path, 'a+').close()

      with open(self.path, 'w+') as storageFile:
         storageFile.write(self.toData(self.object))

      del self.object
      self.isStored = True

   def retrieve(self):
      """Retrieves the item back from storage"""
      if not self.isStored:
         raise ValueError("Item is not stored")

      if not os.path.exists(self.path):
         raise ValueError("This item is stored but the storage file doesn't exsist!!!!")

      with open(self.path, 'r') as storageFile:
         self.object = self.fromData(storageFile.read())

      self.deleteFile()

   def deleteFile(self):
      """Deletes the file where the item was stored"""
      error = None

      try:
         os.remove(self.path)
      except Exception as exception:
         error = exception
      
      if os.path.exists(self.path):
         if error is not None:
            raise FileExistsError("Couldn't delete file") from error
         else:
            raise FileExistsError("The file still exists? (File not deleted)")
      else:
         if self.isStored:
            self.isStored = False

      if error is not None:
         raise error

   def __del__(self):
      """If this object is garbage collected"""
      self.deleteFile()
