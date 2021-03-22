"""4.4 Terms and Definitions"""

import js_interpreter
from js_interpreter import Thing, ThingClass
from js_interpreter.errors import SubclassError
from js_interpreter.TypesAndValues import Type


########################################
#   The actual terms and definitions   #
########################################

Terms = []


def _createTerm(termName, termDefinition, definedAt, parents=None, synonyms=None, alreadyDefinedAs=None, _describes=None):
   """Used for creating terms defined in section 4.4 of the spec"""
   global Terms

   if ': ' not in definedAt:
      definedAt += ': ' + termName

   if alreadyDefinedAs is None:
      term = js_interpreter.createDescriptorWithDefinitionLocation(termName, definedAt, parents=parents, synonyms=synonyms)
   else:
      term = alreadyDefinedAs
      term.addDefinitionLocation(definedAt)
      # WARNING: parents and synonyms not supported in this branch yet
   
   if _describes is not None:
      term._describes = _describes

   term.__doc__ += '\n\n' + termDefinition

   Terms.append(term)
   return term


# TODO: _describes for everything except Type
# This was partly automated - definitions from the specification
TermsAndDefinitions = {
   '4.4.1 implementation-approximated': {
      'definition': 'an implementation-approximated facility is defined in whole or in part by an external source but has a recommended, ideal behaviour in this specification'
   },
   '4.4.2 implementation-defined': {
      'definition': 'an implementation-defined facility is defined in whole or in part by an external source to this specification'
   },
   '4.4.3 host-defined': {
      'definition': 'same as implementation-defined\nNote\n        Editorially, see clause 4.2.\n      ',
      'synonyms': ['implementation-defined']
   },
   '4.4.4 type': {
      'definition': 'set of data values as defined in clause 6',
      'alreadyDefinedAs': Type,
      'not implemented': True
   },
   '4.4.5 primitive value': {
      'definition': 'member of one of the types Undefined, Null, Boolean, Number, BigInt, Symbol, or String as defined in clause 6\nNote\n        A primitive value is a datum that is represented directly at the lowest level of the language implementation.\n      ',
      'not implemented': True
   },
   '4.4.6 object': {
      'definition': 'member of the type Object\nNote\n        An object is a collection of properties and has a single prototype object. The prototype may be the null value.\n      ',
      'not implemented': True
   },
   '6.1.7.2: function object': {
      "definition": '"An object that supports the [[Call]] internal method"',
      "parents": ["object"],
      "definedAt": "6.1.7.2: Object Internal Methods and Internal Slots",
      'not implemented': True
   },
   '4.4.7 constructor': {
      'definition': 
         '4.4.7\n   function object that creates and initializes objects\nNote\n        The value of a constructor\'s \'prototype\' property is a prototype object that is used to implement inheritance and shared properties.\n      ' '\n'
         '6.1.7.2\n   A constructor is an object that supports the [[Construct]] internal method. Every object that supports [[Construct]] must support [[Call]]; that is, every constructor must also be a function object. Therefore, a constructor may also be referred to as a constructor function or constructor function object.\n      ',
      "parents": ["function object"],
      "synonyms": ["constructor function", "constructor function object"],
      "alsoDefinedAt": "6.1.7.2: Object Internal Methods and Internal Slots",
      'not implemented': True
   },
   '4.4.8 prototype': {
      'definition': 'object that provides shared properties for other objects\nNote\n        When a constructor creates an object, that object implicitly references the constructor\'s \'prototype\' property for the purpose of resolving property references. The constructor\'s \'prototype\' property can be referenced by the program expression constructor.prototype, and properties added to an object\'s prototype are shared, through inheritance, by all objects sharing the prototype. Alternatively, a new object may be created with an explicitly specified prototype by using the Object.create built-in function.\n      ',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.9 ordinary object': {
      'definition': 'object that has the default behaviour for the essential internal methods that must be supported by all objects',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.10 exotic object': {
      'definition': 'object that does not have the default behaviour for one or more of the essential internal methods\nNote\n        Any object that is not an ordinary object is an exotic object.\n      ',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.11 standard object': {
      'definition': 'object whose semantics are defined by this specification',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.12 built-in object': {
      'definition': 'object specified and supplied by an ECMAScript implementation\nNote\n        Standard built-in objects are defined in this specification. An ECMAScript implementation may specify and supply additional kinds of built-in objects. A built-in constructor is a built-in object that is also a constructor.\n      ',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.13 undefined value': {
      'definition': 'primitive value used when a variable has not been assigned a value',
      'parents': ["primitive value"],
      'not implemented': True
   },
   '4.4.14 Undefined type': {
      'definition': 'type whose sole value is the undefined value',
      'parents': ['Type'],
      'not implemented': True
   },
   '4.4.15 null value': {
      'definition': 'primitive value that represents the intentional absence of any object value',
      'parents': ["primitive value"],
      'not implemented': True
   },
   '4.4.16 Null type': {
      'definition': 'type whose sole value is the null value',
      'parents': ['Type'],
      'not implemented': True
   },
   '4.4.17 Boolean value': {
      'definition': 'member of the Boolean type\nNote\n        There are only two Boolean values, true and false.\n      ',
      'parents': ["primitive value"],
      'not implemented': True
   },
   '4.4.18 Boolean type': {
      'definition': 'type consisting of the primitive values true and false',
      'parents': ['Type'],
      'not implemented': True
   },
   '4.4.19 Boolean object': {
      'definition': 'member of the Object type that is an instance of the standard built-in Boolean constructor\nNote\n        A Boolean object is created by using the Boolean constructor in a new expression, supplying a Boolean value as an argument. The resulting object has an internal slot whose value is the Boolean value. A Boolean object can be coerced to a Boolean value.\n      ',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.20 String value': {
      'definition': 'primitive value that is a finite ordered sequence of zero or more 16-bit unsigned integer values\nNote\n        A String value is a member of the String type. Each integer value in the sequence usually represents a single 16-bit unit of UTF-16 text. However, ECMAScript does not place any restrictions or requirements on the values except that they must be 16-bit unsigned integers.\n      ',
      'parents': ["primitive value"],
      'not implemented': True
   },
   '4.4.21 String type': {
      'definition': 'set of all possible String values',
      'parents': ['Type'],
      'not implemented': True
   },
   '4.4.22 String object': {
      'definition': 'member of the Object type that is an instance of the standard built-in String constructor\nNote\n        A String object is created by using the String constructor in a new expression, supplying a String value as an argument. The resulting object has an internal slot whose value is the String value. A String object can be coerced to a String value by calling the String constructor as a function (22.1.1.1).\n      ',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.23 Number value': {
      'definition': 'primitive value corresponding to a double-precision 64-bit binary format IEEE 754-2019 value\nNote\n        A Number value is a member of the Number type and is a direct representation of a number.\n      ',
      'parents': ["primitive value"],
      'not implemented': True
   },
   '4.4.24 Number type': {
      'definition': 'set of all possible Number values including the special “Not-a-Number” (NaN) value, positive infinity, and negative infinity',
      'parents': ['Type'],
      'not implemented': True
   },
   '4.4.25 Number object': {
      'definition': 'member of the Object type that is an instance of the standard built-in Number constructor\nNote\n        A Number object is created by using the Number constructor in a new expression, supplying a Number value as an argument. The resulting object has an internal slot whose value is the Number value. A Number object can be coerced to a Number value by calling the Number constructor as a function (21.1.1.1).\n      ',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.26 Infinity': {
      'definition': 'Number value that is the positive infinite Number value',
      'parents': ["primitive value", "Number value"],
      'not implemented': True
   },
   '4.4.27 NaN': {
      'definition': 'Number value that is an IEEE 754-2019 “Not-a-Number” value',
      'parents': ["primitive value", "Number value"],
      'not implemented': True
   },
   '4.4.28 BigInt value': {
      'definition': 'primitive value corresponding to an arbitrary-precision integer value',
      'parents': ["primitive value"],
      'not implemented': True
   },
   '4.4.29 BigInt type': {
      'definition': 'set of all possible BigInt values',
      'parents': ['Type'],
      'not implemented': True
   },
   '4.4.30 BigInt object': {
      'definition': 'member of the Object type that is an instance of the standard built-in BigInt constructor',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.31 Symbol value': {
      'definition': 'primitive value that represents a unique, non-String Object property key',
      'parents': ["primitive value"],
      'not implemented': True
   },
   '4.4.32 Symbol type': {
      'definition': 'set of all possible Symbol values',
      'parents': ['Type'],
      'not implemented': True
   },
   '4.4.33 Symbol object': {
      'definition': 'member of the Object type that is an instance of the standard built-in Symbol constructor',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.34 function': {
      'definition': 'member of the Object type that may be invoked as a subroutine\nNote\n        In addition to its properties, a function contains executable code and state that determine how it behaves when invoked. A function\'s code may or may not be written in ECMAScript.\n      ',
      'parents': ["object"],
      'not implemented': True
   },
   '4.4.35 built-in function': {
      'definition': 'built-in object that is a function\nNote\n        Examples of built-in functions include parseInt and Math.exp. A host or implementation may provide additional built-in functions that are not described in this specification.\n      ',
      'parents': ['built-in object', 'function'],
      'not implemented': True
   },
   '4.4.36 property': {
      'definition': 'part of an object that associates a key (either a String value or a Symbol value) and a value\nNote\n        Depending upon the form of the property the value may be represented either directly as a data value (a primitive value, an object, or a function object) or indirectly by a pair of accessor functions.\n      '
   },
   '4.4.37 method': {
      'definition': 'function that is the value of a property\nNote\n        When a function is called as a method of an object, the object is passed to the function as its this value.\n      ',
      'parents': ['function'],
      'not implemented': True
   },
   '4.4.38 built-in method': {
      'definition': 'method that is a built-in function\nNote\n        Standard built-in methods are defined in this specification. A host or implementation may provide additional built-in methods that are not described in this specification.\n      ',
      'parents': ['method', 'built-in function'],
      'not implemented': True
   },
   '4.4.39 attribute': {
      'definition': 'internal value that defines some characteristic of a property',
      'parents': ['internal value'], # TODO: Internal value
      'not implemented': True
   },
   '4.4.40 own property': {
      'definition': 'property that is directly contained by its object',
      'parents': ['property'],
      'not implemented': True
   },
   '4.4.41 inherited property': {
      'definition': 'property of an object that is not an own property but is a property (either own or inherited) of the object\'s prototype',
      'parents': ['property'], # TODO: Not
      'not implemented': True
   }
}

for term, termDictionary in TermsAndDefinitions.items():
   if "not implemented" in termDictionary and termDictionary["not implemented"] is True:
      continue

   definedAt, termName = term.split(' ', 1)
   termDefinition = termDictionary["definition"]
   synonyms = termDictionary["synonyms"] if "synonyms" in termDictionary else None
   parents = termDictionary["parents"] if "parents" in termDictionary else None
   alreadyDefinedAs = termDictionary["alreadyDefinedAs"] if "alreadyDefinedAs" in termDictionary else None
   _describes = termDictionary["_describes"] if "_describes" in termDictionary else None

   if "definedAt" in termDictionary:
      definedAt = termDictionary["definedAt"]

   if termDefinition is None:
      raise TypeError('A term must have a definition')

   _createTerm(termName, termDefinition, definedAt, parents=parents, synonyms=synonyms, alreadyDefinedAs=alreadyDefinedAs, _describes=_describes)

   if "alsoDefinedAt" in termDictionary:
      for location in termDictionary["alsoDefinedAt"]:
         js_interpreter.descriptors[termName].addDefinitionLocation(location)


del definedAt
del termName
del termDefinition
del synonyms
del parents
del alreadyDefinedAs
del _describes
