from Stmt import *

class Environment:
    def __init__(self) -> None:
        self.values = {}
    

    def define(self, name: str, val: object) -> None:
        self.values[name] = val
    

    def get(self, name: Token) -> object:
        if (name.lexeme in self.values):
            return self.values[name.lexeme]
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")