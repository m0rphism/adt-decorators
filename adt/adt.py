from dataclasses import dataclass
import inspect

def adt(Base):
    return adt_with(export_cons=False)(Base)

def adt_export(Base):
    return adt_with(export_cons=True)(Base)

def adt_with(export_cons: bool):
    def decorator(Base):
        annotations = vars(Base)["__annotations__"]
        Base.__annotations__ = dict()

        def Base_init(self, *args, **kwargs):
            raise TypeError(f"Tryed to construct an ADT instead of one of it's constructor.")
        Base.__init__ = Base_init

        for con_name, con_ty in annotations.items():
            if type(con_ty) == dict:
                params = con_ty
            elif type(con_ty) == tuple or type(con_ty) == list:
                params = { f"_{i+1}": t for (i, t) in enumerate(con_ty) }
            elif type(con_ty) == type:
                params = { "_1": con_ty }
            else:
                raise TypeError(f"ADT with invalid constructor definition {con_name}: {ty}")

            Con = dataclass(type(con_name, (Base, ), { "__annotations__": params }))
            setattr(Base, con_name, Con)

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
