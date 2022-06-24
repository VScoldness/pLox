from Expr import *

class Stmt():
    pass

class ExprStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr
    
    def accept(self, visitor):
        return visitor.visitExprStm(self)

class PrintStmt(Stmt):
    def __init__(self, expr: Expr) -> None:
        self.expr = expr
    
    def accept(self, visitor):
        return visitor.visitPrintStmt(self)

class VarDecl(Stmt):
    def __init__(self, name: Token, indentifier: Expr) -> None:
        self.name = name
        self.indentifier = indentifier
    
    def accept(self, visitor):
        return visitor.visitVarVarDecl(self)

class VisitorStmt:
    def visitExprStm(self):  pass
    def visitPrintStmt(self):   pass
    def visitVarVarDecl(self): pass