# python-ecmascript-interpreter

An implementation of ECMAScript made with Python!

The package name is currently ```js_interpreter``` which is much more convienient if you don't use autocomplete.

## IMPORTANT notes

IMPORTANT: This repo is for educational purposes only.  
If you want to do stuff with JavaScript code in Python, try something else.

IMPORTANT: This implementation is intentionally unoptimized.

## Even more notes

I'm fairly new to Python, so feel free to judge my code.

[This package guide](https://hackernoon.com/pip-install-abra-cadabra-or-python-packages-for-beginners-33a989834975) was really helpful for setting things up.

## What is this?

[The ECMAScript standard](https://tc39.es/ecma262/#sec-conformance) states requirements for "A conforming implementation of ECMAScript"...

- [ ] Must provide and support all
  - [ ] types
  - [ ] values
  - [ ] objects
  - [ ] properties
  - [ ] functions
  - [ ] program syntax
  - [ ] semantics
- [x] interpret source text input in conformance with the with the version of [Unicode]
  - (Done automatically by Python ```string```)
- [ ] If it provides the ```Intl``` API, then it has to implement the most recent specification of the ```Intl``` API
- May also
  - Provide additional everything of the above
  - But not any [Forbidden Extension](https://tc39.es/ecma262/#sec-forbidden-extensions)
- An implementation can choose to implement things in orange boxes.
  - If you implement one (1) thing in an orange box, you must implement all of them to be conforming.

This is an incomplete, and by definition, "non-conforming implementation" of ECMAScript.

You would be hard pressed to find anything that _completely_ conforms, but that's the goal of this project.
