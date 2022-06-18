from Token import *

class Expr():
    def accept(self, visitor): pass

class Binary(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)

class Unary(Expr):
    def __init__(self, operator: Token, right: Expr) -> None:
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)

class Group(Expr):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression
    
    def accept(self, visitor):
        return visitor.visitGroupExpr(self)

class Literal(Expr):
    def __init__(self, val: object) -> None:
        self.val = val
    
    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)


class Visitor:
    def visitBinaryExpr(self):  pass
    def visitUnaryExpr(self):   pass
    def visitGroupExpr(self):   pass
    def visitLiteralExpr(self): pass

