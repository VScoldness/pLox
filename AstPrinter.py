from Expr import *

class AstPrinter(Visitor):
    def out(self, expr: Expr):
        print(expr.accept(self))
        
    
    def visitBinaryExpr(self, expr: Binary) -> str:
        return self.parenthesize(expr.operator.lexeme, [expr.left, expr.right])

    def visitGroupExpr(self, expr: Group) -> str:
        return self.parenthesize("Group", [expr.expression])
    
    def visitLiteralExpr(self, expr: Literal) -> str:
        if (expr.val == None):
            return "nil"
        return str(expr.val)

    def visitUnaryExpr(self, expr: Unary) -> str:
        return self.parenthesize(expr.operator.lexeme, [expr.right])
    
    def parenthesize(self, name: str, exprs: list[Expr]) -> str:
        res = "(" + name
        for expr in exprs:
            res += " "
            res += expr.accept(self)
        res += ")"
        return res

def testForASTP():
    AP     = AstPrinter()
    minus  = Token(TokenType.MINUS, "-", None, 1)
    star   = Token(TokenType.STAR,  "*", None, 1)
    one    = Literal(1.244)
    unary  = Unary(minus, one)
    group  = Group(one)
    binary = Binary(unary, star, group)
    AP.out(one)
    AP.out(unary)
    AP.out(binary)

# testForASTP()
