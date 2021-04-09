# js_interpreter

This package has 3 different types of properties:

- private internals, denoted with a prefix underscore
- public internals, denoted with a starting lowercase letter
- public extenals, denoted with a starting uppercase letter

This also applies to files. And ```__init__.py``` defines
some properties which also conform to that schema.

<!-- Here a property can be either a non-method attribute
     or a method. Includes getters and setters, etc. -->

## Developer notes

Go to the root of this project and run

```powershell
pipreqs --force
```

to generate the requirements.txt file

Run

```powershell
coverage run -m pytest
coverage html
```

for testing and coverage

## Dependency notes

This package depends on `requests` which requires `idna < 3, >= 2.5` which is outdated,
see <https://github.com/psf/requests/issues/5710>
