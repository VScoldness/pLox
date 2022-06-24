from Expr import *

class Interpreter(Visitor):

    def interpreter(self, expression:Expr) -> None:
        try:
            val = self.__evaluate(expression)
            print(val)
        except RuntimeError as error:
            print(f"{error.args[1]} at [line {str(error.args[0].line)}]")


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
            self.__checkNumberOperator(expr.operator, right)
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
            case TokenType.GREATER:
                self.__checkNumberOperator(expr.operator, left, right)            
                return left > right
            case TokenType.GREATER_EQUAL:   
                self.__checkNumberOperator(expr.operator, left, right) 
                return left >= right
            case TokenType.LESS:            
                self.__checkNumberOperator(expr.operator, left, right) 
                return left < right
            case TokenType.LESS_EQUAL:      
                self.__checkNumberOperator(expr.operator, left, right) 
                return left <= right
            case TokenType.BANG_EQUAL:      return left != right
            case TokenType.EQUAL_EQUAL:     return left == right
            case TokenType.MINUS:           
                self.__checkNumberOperator(expr.operator, left, right) 
                return left - right
            case TokenType.SLASH:           
                self.__checkNumberOperator(expr.operator, left, right) 
                return left / right
            case TokenType.STAR:            
                self.__checkNumberOperator(expr.operator, left, right) 
                return left * right
            case TokenType.PLUS:
                if (isinstance(left, float) and isinstance(right, float)) or (isinstance(left, str) and isinstance(right, str)):
                    return left + right
                raise RuntimeError(expr.operator, "Operand must be string or number")
            
    
    def __checkNumberOperator(self, operator: Token, *operands: object) -> None:
        for op in operands:
            if (not isinstance(op, (float, int))):
                raise RuntimeError(operator, "Operand must be number")
        return
    
    
