from Stmt import *

class Environment:
    def __init__(self, enclosing = None) -> None:
        self.__values = {}
        self.__enclosing = enclosing
    

    def define(self, name: str, val: object) -> None:
        self.__values[name] = val
    

    def get(self, name: Token) -> object:
        if (name.lexeme in self.__values):
            return self.__values[name.lexeme]
        if (self.__enclosing):
            return self.__enclosing.get(name)
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
    
    
    def assign(self, name: Token, val: object):
        if (name.lexeme in self.__values):
            self.__values[name.lexeme] = val
            return
        if (self.__enclosing):
            return self.__enclosing.assign(name, val)
        raise RuntimeError(name, f"Undefined variable '{name.lexeme}'.")
