from Expr import *

class Stmt():
    pass

class ExprStmt(Stmt):
    def __init__(self, expr) -> None:
        self.expr = expr
    
    def accept(self, visitor):
        return visitor.visitExprStm(self)

class PrintStmt(Stmt):
    def __init__(self, expr) -> None:
        self.expr = expr
    
    def accept(self, visitor):
        return visitor.visitPrintStmt(self)
    
class VisitorStmt:
    def visitExprStm(self):  pass
    def visitPrintStmt(self):   pass
