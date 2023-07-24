# Overview

This package provides a class decorator for defining
*[Algebraic Data Types (ADTs)](https://en.wikipedia.org/wiki/Algebraic_data_type)* as known from
[Haskell](https://wiki.haskell.org/Algebraic_data_type) (`data`),
[OCaml](https://cs3110.github.io/textbook/chapters/data/algebraic_data_types.html) (`type`), and
[Rust](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html) (`enum`).

## Features

- **Simplicity.** This package exports only a single definition: the
  [`adt`](../reference/#adt.adt) class decorator.

- **Concision.** Constructors are specified via class annotations,
  allowing for syntax comparable to Rust's `enum`s:
  ```python
  from adt import adt

  @adt
  class Event:
      MouseClick: [int, int]
      KeyPress:   {'key': str, 'modifiers': list[str]}
  ```

- **Pattern Matching.** Python's [pattern matching](https://peps.python.org/pep-0636/) via `match` is fully supported (Python >= 3.10).
  ```python
  event = Event.KeyPress(key='a', modifiers=['shift'])
  match event:
      case Event.MouseClick(x, y):    print(f"Clicked at ({x}, {y}).")
      case Event.KeyPress(key, mods): print(f"Pressed key {key}.")
  ```

-   **Support for both named and unnamed constructor fields.** Constructors with

    - named fields, like `KeyPress`, are specified as a `dict[str, type]`;
    - unnamed fields, like `MouseClick`,  are specified as a `list[type]`;
    - a single unnamed field, can also be specified as a `type`;
    - no fields, are specified as the empty list.

- **Getters, Setters, and Instance-Checking.** As an alternative to pattern matching, getter,
  setter, and instance-checking methods are derived, e.g.
  ```python
  if event.is_mouse_click():
      print(f"Clicked at ({event._1}, {event._2}).")
  elif event.is_key_press():
      print(f"Pressed key {event.key}.mods}.")
  ```

- **Constructors are derived as subclasses of the decorated type and
   are themselves decorated with
   [`dataclass`](https://docs.python.org/3/library/dataclasses.html).**
  This derives lots of useful method implementations, e.g. structural
  equality, string-conversion, and ordering.

- **Constructors are namespaced into the ADT class, but can also be additionally exported:**
  ```python
  @adt(export=True)  # <-- No more `Event.` prefixing required.
  class Event:
      MouseClick: [int, int]
      KeyPress:   {'key': str, 'modifiers': list[str]}
      
      def print(self):
          match self:
              MouseClick(x, y):    ... # <-- As promised, no `Event.MouseClick`!
              KeyPress(key, mods): ... # <-- As promised, no `Event.KeyPress`!
  ```


## Translation

The code generated in the above example by the `adt` decorator for the
`Event` ADT behaves equivalent to the following code, with the
exception that the constructor classes are constructed anonymously, so
the global namespace is not even temporarily polluted unless
`@adt(export=True)` is used.

```python
from dataclasses import dataclass

class Event:
    def __init__(self, *args, **kwargs):
        raise TypeError(
            "Tried to construct an ADT instead of one of it's constructors.")

    def is_mouse_click(self) -> bool:
        return isinstance(self, MouseClick)

    def is_key_press(self) -> bool:
        return isinstance(self, KeyPress)

@dataclass
class MouseClick(Expr):
  _1: int
  _2: int

@dataclass
class KeyPress(Expr):
  key: str
  modifiers: list[str]

Expr.MouseClick = MouseClick
Expr.KeyPress   = KeyPress
if not export:
    del MouseClick
    del KeyPress
```

## Related packages

The following compares this package to packages which aim to provide similar functionality:

- [`algebraic-data-types`](https://pypi.org/project/algebraic-data-types/)
  also describes ADTs via class decorators and
  annotations, but does *not* support pattern matching via `match`, as it is aimed
  at older python versions. Also the package does not support named
  constructor parameters.

- [`algebraic-data-type`](https://pypi.org/project/algebraic-data-type/) and
  [`UxADT`](https://pypi.org/project/UxADT/)
  does not support a concise definition via decorators and does not
  support pattern matching via `match`.

- [`choicetypes`](https://pypi.org/project/choicetypes/) implements
  similar functionality, but instead of having subclasses for the constructors,
  the `__init__`-method of the main ADT-Class takes a named argument
  for each constructor variant, which is more verbose, error-prone and
  does not have a straightforward way to support named constructor arguments.

- [`match-variant`](https://pypi.org/project/match-variant/) supports
  pattern matching via `match` and realizes ADTs by inheriting from a
  base class called `Variant` that seems to process the annotations.
  It does not seem to support named constructor parameters and
  methods that check if the ADT is a certain constructor.

- [`py-foldadt`](https://pypi.org/project/py-foldadt/) comes without
  any documentation and has unclear functionality. It defines various
  algebraic structures like semirings with unclear connection to ADTs.
