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

class Block(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements = statements
    
    def accept(self, visitor):
        return visitor.visitBlock(self)

class IF(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch
    
    def accept(self, visitor):
        return visitor.visitIF(self)

class WhileStmt(Stmt):
    def __init__(self, condition: Expr, body: Stmt) -> None:
        self.condition = condition
        self.body = body
    
    def accept(self, visitor):
        return visitor.visitWhileStmt(self)

class FuncStmt(Stmt):
    def __init__(self, name: Token, params: list[Token], body: list[Stmt]) -> None:
        self.name = name
        self.params = params
        self.body = body
    
    def accept(self, visitor):
        return visitor.visitFuncStmt(self)

class ReturnStmt(Stmt):
    def __init__(self, keyword: Token, val: Expr):
        self.keyword = keyword
        self.val = val

    def accept(self, visitor):
        return visitor.visitReturnStmt(self)

class VisitorStmt:
    def visitExprStm(self):     pass
    def visitPrintStmt(self):   pass
    def visitVarVarDecl(self):  pass
    def visitBlock(self):       pass
    def visitIF(self):          pass
    def visitWhileStmt(self):   pass
    def visitFuncStmt(self):    pass
    def visitReturnStmt(self):  pass
