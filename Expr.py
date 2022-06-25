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


class Variable(Expr):
    def __init__(self, name: Token) -> None:
        self.name = name
    
    def accept(self, visitor):
        return visitor.visitVariableExpr(self)

class Assign(Expr):
    def __init__(self, name: Token, val: Expr) -> None:
        self.name = name
        self.val  = val
    
    def accept(self, visitor):
        return visitor.visitAssignExpr(self)
    

class Logical(Expr):
    def __init__(self, left: Expr, operator: Token, right: Expr) -> None:
        self.left = left
        self.operator = operator
        self.right = right
    
    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)
        



class Visitor:
    def visitBinaryExpr(self):  pass
    def visitUnaryExpr(self):   pass
    def visitGroupExpr(self):   pass
    def visitLiteralExpr(self): pass
    def visitVariableExpr(self): pass
    def visitAssignExpr(self):  pass
    def visitLogicalExpr(self): pass

