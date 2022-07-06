from LoxCallable import *
from Environment import *

class LoxFuntion(LoxCallable):
    def __init__(self, declaration: FuncStmt, closure: Environment) -> None:
        self.declaration = declaration
        self.closure = closure
    
    # override
    def call(self, interpreter, arguments: list[object]) -> object:
        env = Environment(self.closure)
        for idx in range(len(arguments)):
            env.define(self.declaration.params[idx].lexeme, arguments[idx])
        try:
            interpreter.executeBlock(self.declaration.body, env)
        except RuntimeError as error:
            print(f"{error.args[1]} at [line {str(error.args[0].line)}]")
        except Exception as error:
            return error.args[0]
        
        return None
    
    # override
    def arity(self) -> int:
        return len(self.declaration.params)

    # override
    def toString(self) -> str:
        return f"<fn {self.declaration.name.lexeme}>"