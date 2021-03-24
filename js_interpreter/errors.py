
class SubclassError (ValueError):
   """When someone subclassed wrong"""
   pass


class FiniteCreationError (ValueError, TypeError):
   """When a type can only create a limited number of values"""
   pass
