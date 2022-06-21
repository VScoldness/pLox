from Expr import *

class Interpreter(Visitor):

    def __evaluate(self, expr: Expr):
        return expr.accept(self)


    # override
    def visitLiteralExpr(self, expr: Literal):
        return expr.val
    

    # override
    def visitGroupExpr(self, expr: Group):
        return self.__evaluate(expr.expression)
    

    # override
    def visitUnaryExpr(self, expr: Unary):
        right = self.__evaluate(expr.right)
        if (expr.operator.type == TokenType.MINUS):
            return -1 * right
        elif (expr.operator.type == TokenType.BANG):
            return not right
        else:
            raise "Unexpected operator in unary token" # how to handle error !!!
    

    # override
    def visitBinaryExpr(self, expr: Binary):
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        match expr.operator.type:
            case TokenType.GREATER:         return left > right
            case TokenType.GREATER_EQUAL:   return left >= right
            case TokenType.LESS:            return left < right
            case TokenType.LESS_EQUAL:      return left <= right
            case TokenType.BANG_EQUAL:      return left != right
            case TokenType.EQUAL_EQUAL:     return left == right
            case TokenType.MINUS:           return left - right
            case TokenType.SLASH:           return left / right
            case TokenType.STAR:            return left * right
            case TokenType.PLUS:            return left + right
            
    

    
