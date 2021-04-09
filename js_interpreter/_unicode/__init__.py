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
def _HTTP_Header_to_datetime(httpDatetime):
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
   lines = [line.strip() for line in lines]  # Equivalent to .trim() in JS

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
   latestPropertyListDataRequest = requests.get(
       "https://www.unicode.org/Public/14.0.0/ucd/PropList-14.0.0d9.txt")
   latestPropertyListDataRequestTime = _HTTP_Header_to_datetime(
       latestPropertyListDataRequest.headers.get('Date', None))
   PropertyListDataLastModified = _HTTP_Header_to_datetime(
       latestPropertyListDataRequest.headers.get('Last-Modified', None))
   PropertyListData = getUnicodePropertyListData()


latestPropertyListDataRequest = None
latestPropertyListDataRequestTime = None
PropertyListDataLastModified = None
PropertyListData = None
updatePropertyListData()


######################################
#       Handy Unicode Functions      #
######################################

# def codePointsOfString (string):
#    return [ord(character) for character in string]


######################################
#     Unicode Category Functions     #
######################################

UNICODE_GENERAL_CATEGORY_VALUES = {
    "Uppercase_Letter": {
        "Abbreviation": "Lu",
        "Description": "an uppercase letter"
    },
    "Lowercase_Letter": {
        "Abbreviation": "Ll",
        "Description": "a lowercase letter"
    },
    "Titlecase_Letter": {
        "Abbreviation": "Lt",
        "Description": "a digraphic character, with first part uppercase"
    },
    "Cased_Letter": {
        "Abbreviation": "LC",
        "Description": ("Lu", "Ll", "Lt")
    },
    "Modifier_Letter": {
        "Abbreviation": "Lm",
        "Description": "a modifier letter"
    },
    "Other_Letter": {
        "Abbreviation": "Lo",
        "Description": "other letters, including syllables and ideographs"
    },
    "Letter": {
        "Abbreviation": "L",
        "Description": ("Lu", "Ll", "Lt", "Lm", "Lo")
    },
    "Nonspacing_Mark": {
        "Abbreviation": "Mn",
        "Description": "a nonspacing combining mark (zero advance width)"
    },
    "Spacing_Mark": {
        "Abbreviation": "Mc",
        "Description": "a spacing combining mark (positive advance width)"
    },
    "Enclosing_Mark": {
        "Abbreviation": "Me",
        "Description": "an enclosing combining mark"
    },
    "Mark": {
        "Abbreviation": "M",
        "Description": ("Mn", "Mc", "Me")
    },
    "Decimal_Number": {
        "Abbreviation": "Nd",
        "Description": "a decimal digit"
    },
    "Letter_Number": {
        "Abbreviation": "Nl",
        "Description": "a letterlike numeric character"
    },
    "Other_Number": {
        "Abbreviation": "No",
        "Description": "a numeric character of other type"
    },
    "Number": {
        "Abbreviation": "N",
        "Description": ("Nd", "Nl", "No")
    },
    "Connector_Punctuation": {
        "Abbreviation": "Pc",
        "Description": "a connecting punctuation mark, like a tie"
    },
    "Dash_Punctuation": {
        "Abbreviation": "Pd",
        "Description": "a dash or hyphen punctuation mark"
    },
    "Open_Punctuation": {
        "Abbreviation": "Ps",
        "Description": "an opening punctuation mark (of a pair)"
    },
    "Close_Punctuation": {
        "Abbreviation": "Pe",
        "Description": "a closing punctuation mark (of a pair)"
    },
    "Initial_Punctuation": {
        "Abbreviation": "Pi",
        "Description": "an initial quotation mark"
    },
    "Final_Punctuation": {
        "Abbreviation": "Pf",
        "Description": "a final quotation mark"
    },
    "Other_Punctuation": {
        "Abbreviation": "Po",
        "Description": "a punctuation mark of other type"
    },
    "Punctuation": {
        "Abbreviation": "P",
        "Description": ("Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po")
    },
    "Math_Symbol": {
        "Abbreviation": "Sm",
        "Description": "a symbol of mathematical use"
    },
    "Currency_Symbol": {
        "Abbreviation": "Sc",
        "Description": "a currency sign"
    },
    "Modifier_Symbol": {
        "Abbreviation": "Sk",
        "Description": "a non-letterlike modifier symbol"
    },
    "Other_Symbol": {
        "Abbreviation": "So",
        "Description": "a symbol of other type"
    },
    "Symbol": {
        "Abbreviation": "S",
        "Description": ("Sm", "Sc", "Sk", "So")
    },
    "Space_Separator": {
        "Abbreviation": "Zs",
        "Description": "a space character (of various non-zero widths)"
    },
    "Line_Separator": {
        "Abbreviation": "Zl",
        "Description": "U+2028 LINE SEPARATOR only"
    },
    "Paragraph_Separator": {
        "Abbreviation": "Zp",
        "Description": "U+2029 PARAGRAPH SEPARATOR only"
    },
    "Separator": {
        "Abbreviation": "Z",
        "Description": ("Zs", "Zl", "Zp")
    },
    "Control": {
        "Abbreviation": "Cc",
        "Description": "a C0 or C1 control code"
    },
    "Format": {
        "Abbreviation": "Cf",
        "Description": "a format control character"
    },
    "Surrogate": {
        "Abbreviation": "Cs",
        "Description": "a surrogate code point"
    },
    "Private_Use": {
        "Abbreviation": "Co",
        "Description": "a private-use character"
    },
    "Unassigned": {
        "Abbreviation": "Cn",
        "Description": "a reserved unassigned code point or a noncharacter"
    },
    "Other": {
        "Abbreviation": "C",
        "Description": ("Cc", "Cf", "Cs", "Co", "Cn")
    }
}


def IsInCategory(char, category):
   """
   Checks if a given character is in a specific unicode category.
   See http://www.unicode.org/reports/tr44/#General_Category_Values
   """
   category = UNICODE_GENERAL_CATEGORY_VALUES[category]
   if unicodedata.category(char) == category["Abbreviation"]:
      return True
   elif isinstance(category["Description"], tuple):
      return unicodedata.category(char) in category["Description"]

   return False


def IsInCategories(char, categories):
   """
   Checks if a given character is in a group of multiple categories
   Similar to <IsInCategory>
   """
   for category in categories:
      if IsInCategory(char, category):
         return True

   return False


def HasProperty(char, property_name):
   """
   Checks if a given character has a unicode property
   See https://www.unicode.org/reports/tr31/#Table_Lexical_Classes_for_Identifiers
   See https://www.unicode.org/reports/tr44/tr44-26.html#Other_ID_Continue
   See https://www.unicode.org/Public/14.0.0/ucd/PropList-14.0.0d9.txt
   """
   return ord(char) in PropertyListData[property_name]


def HasPropertyID_Start(char):
   """
   Checks if a given character has the unicode property ID_Start;
      A Letter, or a Letter_Number, or Other_ID_Start,
      but not Pattern_Syntax or Pattern_White_Space

   See <HasProperty>
   """
   if IsInCategory(char, ("Letter", "Letter_Number")) or HasProperty(char, "Other_ID_Start"):
      return not (HasProperty(char, "Pattern_Syntax") or HasProperty(char, "Pattern_White_Space"))
   return False


def HasPropertyID_Continue(char):
   """
   Checks if a given character has the unicode property ID_Start;
      which includes
      - ID_Start
      - Nonspacing_Mark
      - Spacing_Mark
      - Decimal_Number
      - Connector_Punctuation
      - Other_ID_Continue
      but not Pattern_Syntax or Pattern_White_Space

   See <HasProperty>
   """
   huge_condition = (
       HasPropertyID_Start(char) or
       IsInCategories(char, ("Nonspacing_Mark", "Spacing_Mark", "Decimal_Number", "Connector Punctuation")) or
       HasProperty(char, "Other_ID_Continue")
   )

   if huge_condition:
      return not (HasProperty(char, "Pattern_Syntax") or HasProperty(char, "Pattern_White_Space"))
   return False
