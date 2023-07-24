from adt import adt, adt_export

@adt_export
class Expr:
    Var: str                           # Single Unnamed Con Arg
    Abs: [str, 'Expr']                 # Multiple Unnamed Con Args
    App: {'e1': 'Expr', 'e2': 'Expr'}  # Multiple Named Con Args

    def __str__(self) -> str:
        match self:
            case Var(x):      return x
            case Abs(x, e):   return f"(λ{x}. {e})"
            case App(e1, e2): return f"({e1} {e2})"

print("\n===== Constructors NS ==")
print(Expr.Var("x"))
print(Expr.Abs("x", "y"))
print(Expr.App("x", "y"))

print("\n===== Constructors =====")
print(Var("x"))
print(Abs("x", "y"))
print(App("x", "y"))

print("\n===== Predicates =======")
print(Var("x").is_var())
print(Abs("x", "y").is_app())

print("\n===== Repr =============")
print(repr(Var("x")))
print(repr(Abs("x", "y")))
print(repr(App("x", "y")))

print("\n===== Field Access =====")
print(Var("x")._1)
print(Abs("x", "y")._1)
print(App("x", "y").e1)

print("\n===== Subtyping ========")
print(isinstance(App("x", "y"), Expr))

print("\n===== Importing ========")

def expr_to_str(e: Expr) -> str:
    match e:
        case Var(x): return x
        case Abs(x, e): return f"(λ{x}. {expr_to_str(e)})"
        case App(e1, e2): return f"({expr_to_str(e1)} {expr_to_str(e2)})"

id = Abs("x", Var("x"))
print(expr_to_str(id))
