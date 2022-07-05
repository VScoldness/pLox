from LoxCallable import *
from Environment import *

class LoxFuntion(LoxCallable):
    def __init__(self, declaration: FuncStmt) -> None:
        self.declaration = declaration
    
    # override
    def call(self, interpreter, arguments: list[object]) -> object:
        env = Environment(interpreter.globals)
        for idx in range(len(arguments)):
            env.define(self.declaration.params[idx].lexeme, arguments[idx])
        interpreter.executeBlock(self.declaration.body, env)
        return None
    
    # override
    def arity(self) -> int:
        return len(self.declaration.params)

    # override
    def toString(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"