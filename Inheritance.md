# Inheritance

This file shows the inheritance of everything, starting from Thing.

## Syntax

```python
Class
--- Subclass

Class
= AttributeOfClass (but not MethodOfClass)

Metaclass
--> Class

Class
> InstanceClass

# A class without a `>` is equivalent to
Class
> Class


Class
| PropertyOrMethod
? Optional Property or Method

Class
? Optional Property or Method
--- Subclass
    + Required Property or Method

Class
! DontUseThisClassErrorType

methodOrFunction()
> ReturnValueType
! ErrorValueType

variableOrAttribute = ExactValue
variableOrAttribute: ValueType
variableOrAttribute: {
  [key: ValueType]: ValueTypeOrValue
}
```

## Tree

```python
CURRENT_IMPLEMENTATION_PROGRESS: str & HeaderOfEcmaScriptSpec
descriptors = {[key: Descriptor.name]: Descriptor}
described_by = [SomeImplementationDescriptor]
defined_at = None

isThingClassOrDescriptorClass()
> bool

isThing()
> bool

isDescriptor()
> bool

getDescriptorAndCreateIfUndefined()
> Descriptor

parse()
! NotImplementedError

run()
! NotImplementedError

Thing
= described_by
= defined_at
? name
| described_by
| defined_at
| addDescriptor()
| isDescribedBy()
| setDefinitionLocation()
| addDefinitionLocation()
--- Descriptor
    = described_by
    = defined_at
    + name
    | _parents
    | _is_also
    | __doc__
    | __str__()
    | __repr__()
    | describe()
    | describes()


```
