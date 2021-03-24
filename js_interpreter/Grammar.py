from js_interpreter import Thing, ThingClass
from js_interpreter.errors import SubclassError
from js_interpreter._unique import Unique


# IDEA: ProductionList
class ContextFree_Grammar (Thing, metaclass=ThingClass):
   values = []

   def __init__(self, name, productions=None, goal_symbols=None):
      super().__init__(name=name)

      if productions is None:
         self.productions = []
      else:
         self.productions = productions

      if goal_symbols is None:
         self.goal_symbols = []
      else:
         self.goal_symbols = goal_symbols


class LeftHandSide (Thing, metaclass=ThingClass):
   pass

class RightHandSide (Thing, metaclass=ThingClass):
   pass





# TODO: Parameters
class Production (Thing, metaclass=ThingClass):
   def __init__(self, leftHand_Side, rightHand_Side):
      self.leftHand_Side = leftHand_Side
      self.rightHand_Side = rightHand_Side

      self.hasAlternatives = isinstance(rightHand_Side, list)


class ChainProduction (Production):
   pass


# Abstract Symbol?
# italic
# descriptive phrase = sans serif if too many alternatives
class NonTerminal (Thing, metaclass=ThingClass):
   pass

# fixed width
class Terminal (Thing, metaclass=ThingClass):
   pass

class GoalSymbol (NonTerminal):
   pass

class UnicodeCodePoint (Terminal):
   pass


# See 5.1.1
class Language (Thing, metaclass=ThingClass):
   def __init__ (self, aContextFree_GrammarOrGoalSymbol):
      pass


Lexical_Grammar = ContextFree_Grammar('Lexical Grammar')
RegExp_Grammar = ContextFree_Grammar('RegExp Grammar')
Numeric_String_Grammar = ContextFree_Grammar('Numeric String Grammar')
Syntactic_Grammar = ContextFree_Grammar('Syntactic Grammar') # Ohhh, this grammar has Script or Module

# tokens
# Revisit 5.1.2

# 5.1.4
# Parse tree,
# Parse Node, each of which is an instance of a symbol in the grammar
# and if that Parse Node is an instance of a non-terminal, it is also an instance of some production

# parser invocation

# params
# optional()
# dependent()

# lookahead
# empty
# no lineterminator (other any amount)
