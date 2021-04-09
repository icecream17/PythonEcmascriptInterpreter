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


def openStorageFile(filename, *args, **kwargs):
   """Returns the result of opening the file at filename"""
   return open(os.path.join(STORAGE_DIRECTORY, filename), *args, **kwargs)
