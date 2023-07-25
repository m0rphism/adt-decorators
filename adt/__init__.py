"""Provides class decorators for Algebraic Data Types (ADTs)
"""

__version__ = "0.2.11"
__author__ = 'Hannes Saffrich'

from dataclasses import dataclass
import inspect

def adt(Class=None, export=False, **kwargs):
    """Class-decorator for Algebraic Data Types (ADTs).

    This function is overloaded to allow both `@adt` and
    `@adt(OPTIONS)` annotations. In the case of `@adt` only the
    `Class` argument is supplied and the decorator is *called*;
     in the case of `@adt(export=True)` only the other arguments are
     supplied and the decorator is *returned*.

    Arguments:
        export:
            if `False`, only define the constructor classes as fields of the decorated class;
            if `True`, also define the constructor classes in the global namespace.
        **kwargs: 
            additional passed keyword arguments passed to dataclass decorator. 

    Examples:
        >>> @adt
        ... class Expr:
        ...     Var: str                           # Single Unnamed Con Arg
        ...     Abs: [str, 'Expr']                 # Multiple Unnamed Con Args
        ...     App: {'e1': 'Expr', 'e2': 'Expr'}  # Multiple Named Con Args
        ... 
        ...     def __str__(self) -> str:
        ...         match self:
        ...             case Expr.Var(x):      return x
        ...             case Expr.Abs(x, e):   return f"(λ{x}. {e})"
        ...             case Expr.App(e1, e2): return f"({e1} {e2})"
        >>> id_expr = Expr.Abs("x", Expr.Var("x"))
        >>> str(id_expr)
        '(λx. x)'

        >>> @adt(export=True)
        ... class Expr:
        ...     Var: str                           # Single Unnamed Con Arg
        ...     Abs: [str, 'Expr']                 # Multiple Unnamed Con Args
        ...     App: {'e1': 'Expr', 'e2': 'Expr'}  # Multiple Named Con Args
        ... 
        ...     def __str__(self) -> str:
        ...         match self:
        ...             case Var(x):      return x
        ...             case Abs(x, e):   return f"(λ{x}. {e})"
        ...             case App(e1, e2): return f"({e1} {e2})"
        >>> id_expr = Abs("x", Var("x"))
        >>> str(id_expr)
        '(λx. x)'

        >>> @adt(frozen=True)
        ... class Expr:
        ...     Var: str                           # Single Unnamed Con Arg
        ...     Abs: [str, 'Expr']                 # Multiple Unnamed Con Args
        ...     App: {'e1': 'Expr', 'e2': 'Expr'}  # Multiple Named Con Args
        ... 
        >>> var = Expr.Var("x")
        >>> var._0 = "y" # error!
    """
    decorator = adt_with(export, **kwargs)
    return decorator if Class is None else decorator(Class)

def adt_with(export_cons: bool, **kwargs):
    def decorator(Base):
        annotations = vars(Base)["__annotations__"]
        Base.__annotations__ = dict()

        def Base_init(self, *args, **kwargs):
            raise TypeError(f"Tryed to construct an ADT instead of one of it's constructor.")
        Base.__init__ = Base_init
        Base.constructors = dict()

        for con_name, con_ty in annotations.items():
            if type(con_ty) == dict:
                params = con_ty
            elif type(con_ty) == tuple or type(con_ty) == list:
                params = { f"_{i+1}": t for (i, t) in enumerate(con_ty) }
            elif type(con_ty) == type:
                params = { "_1": con_ty }
            else:
                raise TypeError(f"ADT with invalid constructor definition {con_name}: {con_ty}")

            Con = dataclass(type(con_name, (Base, ), { "__annotations__": params }), **kwargs)
            setattr(Base, con_name, Con)
            Base.constructors[con_name] = Con

            def is_con_gen(Con):
                def is_con(self) -> bool:
                    return isinstance(self, Con)
                return is_con
            is_con_name = "is_" + upper_camel_to_snake(con_name)
            setattr(Base, is_con_name, is_con_gen(Con))

        def export_cons_fn():
            frame = inspect.currentframe()
            if frame is None:
                raise RuntimeError('Cannot inspect stack frames')
            frame = frame.f_back
            while frame is not None:
                for con_name in annotations:
                    frame.f_globals[con_name] = getattr(Base, con_name)
                frame = frame.f_back
        setattr(Base, "export_cons", export_cons_fn)

        if export_cons:
            export_cons_fn()


        # def import_cons():
        #     frame = inspect.currentframe()
        #     if frame is None:
        #         raise RuntimeError('Cannot inspect stack frames')
        #     frame = frame.f_back
        #     if frame is None:
        #         raise RuntimeError('Cannot inspect stack frames')
        #     # if '__name__' in frame.f_locals:
        #     #     print("GLOBAL")
        #     #     scope = frame.f_locals
        #     # else:
        #     #     scope = frame.f_globals
        #     scope = frame.f_builtins
        #     # scope = frame.f_globals
        #     for con_name in annotations:
        #         scope[con_name] = getattr(Base, con_name)

        # setattr(Base, "import_cons", import_cons)

        return Base
    return decorator

def upper_camel_to_snake(s: str) -> str:
    out = ""
    for i, c in enumerate(s):
        if c.isupper():
            if i != 0:
                out += "_"
            out += c.lower()
        else:
            out += c
    return out
