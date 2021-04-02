"""
Provides unicode support because JavaScript code is encoded with Unicode.
"""

from datetime import datetime
from email.utils import parsedate
import unicodedata
import requests


######################################
#    HTTP Requesting Unicode Data    #
######################################

# Thanks to https://stackoverflow.com/questions/1471987/how-do-i-parse-an-http-date-string-in-python
def _datetimeFromHTTPheader(httpDatetime):
   if httpDatetime is None:
      return None
   return datetime(*parsedate(httpDatetime)[:6])


def getUnicodePropertyListData():
   def _removeComments(line):
      index = line.find('#')
      if index == -1:
         return line
      else:
         return line[:index]


   def _toRangeAndName(line):
      line = {
         "range": line[0].strip(),
         "name": line[1].strip()
      }

      if ".." in line["range"]:
         start, end = [int(part, 16) for part in line["range"].split('..')]
         line["range"] = list(range(start, end + 1))
      else:
         # An array with only one code point
         line["range"] = [int(line["range"], 16)]

      return line



   lines = latestPropertyListDataRequest.text.split('\n')
   lines = [_removeComments(line) for line in lines]
   lines = [line.strip() for line in lines] # Equivalent to .trim() in JS

   # 1. Filters lines that don't have ';'
   # 2. Splits lines into two parts: the range and the name
   lines = [line.split(';') for line in lines if ';' in line]
   lineData = [_toRangeAndName(line) for line in lines]
   data = {}

   for element in lineData:
      if element['name'] not in data:
         data[element['name']] = []

      data[element['name']] += element['range']

   for key in data:
      data[key] = list(set(data[key]))

   return data


def updatePropertyListData():
   global latestPropertyListDataRequest
   global latestPropertyListDataRequestTime
   global PropertyListDataLastModified
   global PropertyListData
   latestPropertyListDataRequest = requests.get("https://www.unicode.org/Public/14.0.0/ucd/PropList-14.0.0d9.txt")
   latestPropertyListDataRequestTime = _datetimeFromHTTPheader(latestPropertyListDataRequest.headers.get('Date', None))
   PropertyListDataLastModified = _datetimeFromHTTPheader(latestPropertyListDataRequest.headers.get('Last-Modified', None))
   PropertyListData = getUnicodePropertyListData()


latestPropertyListDataRequest = None
latestPropertyListDataRequestTime = None
PropertyListDataLastModified = None
PropertyListData = None
updatePropertyListData()


######################################
#       Handy Unicode Functions      #
######################################

def codePointsOfString (string):
   return [ord(character) for character in string]



######################################
#     Unicode Category Functions     #
######################################


def IsInCategorySpaceSeperator(char):
   return unicodedata.category(char) == 'Zs'


def IsInCategoryLetter(char):
   return unicodedata.category(char) in ["Lu", "Ll", "Lt", "Lm", "Lo"]


def IsInCategoryLetterNumber(char):
   return unicodedata.category(char) == 'Nl'


def IsInCategoryNonspacingMark(char):
   return unicodedata.category(char) == 'Mn'


def IsInCategorySpacingMark(char):
   return unicodedata.category(char) == 'Mc'


def IsInCategoryDecimalNumber(char):
   return unicodedata.category(char) == 'Nd'


def IsInCategoryConnectorPunctuation(char):
   return unicodedata.category(char) == 'Pc'


# See https://www.unicode.org/reports/tr31/#Table_Lexical_Classes_for_Identifiers
# See https://www.unicode.org/reports/tr44/tr44-26.html#Other_ID_Continue
# See https://www.unicode.org/Public/14.0.0/ucd/PropList-14.0.0d9.txt

def HasProperty(property_name, char):
   return ord(char) in PropertyListData[property_name]


# A letter, or a letter number, or Other_ID_Start,
# but not Pattern_Syntax or Pattern_White_Space

def HasPropertyID_Start(char):
   if IsInCategoryLetter(char) or IsInCategoryLetterNumber(char) or HasProperty("Other_ID_Start", char):
      return not (HasProperty("Pattern_Syntax", char) or HasProperty("Pattern_White_Space", char))
   return False


# Same as ID_Start, but also Nonspacing mark, Spacing mark, Decimal number, Connector Punctuation, and Other_ID_Continue
# Also excludes Pattern_Syntax and Pattern_White_Space

def HasPropertyID_Continue(char):
   huge_condition = (
      HasPropertyID_Start(char) or
      IsInCategoryNonspacingMark(char) or
      IsInCategorySpacingMark(char) or
      IsInCategoryDecimalNumber(char) or
      IsInCategoryConnectorPunctuation(char) or
      HasProperty("Other_ID_Continue", char)
   )

   if huge_condition:
      return not (HasProperty("Pattern_Syntax", char) or HasProperty("Pattern_White_Space", char))
   return False
