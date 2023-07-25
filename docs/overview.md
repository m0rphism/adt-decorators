# Overview

This package provides a class decorator for defining
*[Algebraic Data Types (ADTs)](https://en.wikipedia.org/wiki/Algebraic_data_type)* as known from
[Haskell](https://wiki.haskell.org/Algebraic_data_type) (`data`),
[OCaml](https://cs3110.github.io/textbook/chapters/data/algebraic_data_types.html) (`type`), and
[Rust](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html) (`enum`).

[//]: # (INSTALL_BEGIN)
## Installation

The package is on [PyPI](https://pypi.org/project/adt-decorators/)
and [github](https://github.com/m0rphism/adt-decorators)
and can be installed via
```bash
pip install adt-decorators
```
[//]: # (INSTALL_END)

## Features

- **Simplicity.** This package exports only a single definition: the
  [`adt`](../reference/#adt.adt) class decorator:
  ```python
  from adt import adt
  ```

- **Concision.** Constructors are specified via class annotations,
  allowing for syntax comparable to Rust's `enum`s:
  ```python
  @adt
  class Event:
      MouseClick: [int, int]
      KeyPress:   {'key': str, 'modifiers': list[str]}
  ```

- **Pattern Matching** via [`match`](https://peps.python.org/pep-0636/) is fully supported (Python >= 3.10):
  ```python
  event = Event.KeyPress(key='a', modifiers=['shift'])
  match event:
      case Event.MouseClick(x, y):    print(f"Clicked at ({x}, {y}).")
      case Event.KeyPress(key, mods): print(f"Pressed key {key}.")
  ```

-   **Named and unnamed constructor fields** are supported:

    - Constructors with named fields, like `KeyPress`, are specified as a `dict[str, type]`;
    - Constructors with unnamed fields, like `MouseClick`,  are specified as a `list[type]`;
    - Constructors with a single unnamed field can also be specified as a `type`;
    - Constructors with no fields are specified as the empty list.

- **Getters, Setters, and Instance-Checking** methods are derived as an alternative to pattern matching, e.g.
  ```python
  if event.is_mouse_click():
      print(f"Clicked at ({event._1}, {event._2}).")
  elif event.is_key_press():
      print(f"Pressed key {event.key}.")
  ```

-   **Constructors are customizable dataclasses.**
    The [`dataclass`](https://docs.python.org/3/library/dataclasses.html)
    decorator derives many useful method implementations,
    e.g. structural equality and string-conversion.

    Additonal keyword arguments to `adt` are forwarded as keyword
    arguments to the `dataclass` annotations of all constructors:
    ```python
    @adt(frozen=True)  # <-- Use @dataclass(frozen=True) for all constructors.
    class Event:
        MouseClick: [int, int]
        KeyPress:   {'key': str, 'modifiers': list[str]}

    event = Event.MouseClick(5, 10)
    event._0 = 42 # Error! Constructor dataclass is frozen. 
    ```

- **Constructors inherit from the decorated type.**
  Making the constructors inherit from the decorated class, allows to
  define methods with pattern matching directly in the decorated class
  and call them on objects of the constructor classes:
  ```python
  @adt
  class Event:
      MouseClick: [int, int]
      KeyPress:   {'key': str, 'modifiers': list[str]}
      
      def print(self):
          match self:
              case Event.MouseClick(x, y):    print(f"Clicked at ({event._1}, {event._2}).")
              case Event.KeyPress(key, mods): print(f"Pressed key {event.key}.")

  Event.MouseClick(5, 10).print()
  ```

- **Constructors can be exported into the global namespace.**
  ```python
  @adt(export=True)  # <-- Makes `Event.` prefixes optional for constructors.
  class Event:
      MouseClick: [int, int]
      KeyPress:   {'key': str, 'modifiers': list[str]}
      
      def print(self):
          match self:
              case MouseClick(x, y):    ... # <-- As promised: no `Event.MouseClick`!
              case KeyPress(key, mods): ... # <-- As promised: no `Event.KeyPress`!
  ```

- **Reflection.**
  The decorated class has a static field `constructors: dict[str, type]`
  which maps the constructor names to their classes, e.g.
  ```python
  key_event = Event.constructors['KeyPress'](key='a', modifiers=['shift'])
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
        return isinstance(self, Event.MouseClick)

    def is_key_press(self) -> bool:
        return isinstance(self, Event.KeyPress)

@dataclass
class MouseClick(Event):
  _1: int
  _2: int

@dataclass
class KeyPress(Event):
  key: str
  modifiers: list[str]

Event.MouseClick = MouseClick
Event.KeyPress   = KeyPress
if not export:
    del MouseClick
    del KeyPress

Event.constructors = {
    'MouseClick': Event.MouseClick,
    'KeyPress': Event.KeyPress,
}
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
