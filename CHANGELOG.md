# CHANGELOG

*Note:* Versions, which are not listed here, contain only updates to the documentation.

- **0.2.11** Added possibility to customize the arguments to the
  `@dataclass` annotation for the constructor classes.

- **0.2.9** Added basic reflection capabilities: Each class decorated
  with `@adt` has a static field `constructors: dict[str, type]`,
  which maps constructor names to their classes.

- **0.2.0** Unified API by having `@adt` and `@adt(export=True)`
  instead of `@adt` and `@adt_export`.

- **0.1.1** Basic functionality
