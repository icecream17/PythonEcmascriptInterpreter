from js_interpreter import Thing, ThingClass


class Algorithm (Thing, metaclass=ThingClass):
   def __init__(self, parameters, steps, **kwargs):
      super().__init__(**kwargs)
      self.parameters = parameters
      self.steps = steps


# Contains other steps
class AlgorithmStep (Thing, metaclass=ThingClass):
   pass


class IfPredicate (AlgorithmStep):
   pass

class ElsePredicate (AlgorithmStep):
   pass

class ElseIfPredicate (IfPredicate, ElsePredicate):
   pass

class Assertion (AlgorithmStep):
   pass

class Return (AlgorithmStep):
   pass


class AlgorithmStepValue (Thing, metaclass=ThingClass):
   pass


# Explicit copy
class DeclareNamedAlias (AlgorithmStep):
   pass

class ModifyNamedAlias (AlgorithmStep):
   pass

class GetNamedAlias (AlgorithmStepValue):
   pass


# Named
class AbstractOperation (Algorithm):
   pass

class CallAbstractOperation (AlgorithmStepValue):
   pass




class SyntaxDirectedOperation (Thing, metaclass=ThingClass):
   def __init__(self, algorithmsAssociatedWithProductionsAndPossiblyAlternative):
      pass


class RuntimeSemantics (Algorithm):
   def __init__(self, definedBy):
      if not isinstance(definedBy, (AbstractOperation, SyntaxDirectedOperation)):
         raise TypeError("A runtime semantics must be defined by an abstract operation or syntax-directed operation")


# TODO:
# Normal Completion
# Completion
# CompletionValue reference is usually equivalent to value itself, see last part of 5.2.3.1
# Throw
# ThrowCompletion
# ReturnIfAbrupt
# ExclaimPrefix
# StaticSemantics
# --- EarlyErrorRule

# MathematicalOperations
