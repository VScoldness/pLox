from LoxFunction import *


class Interpreter(Visitor, VisitorStmt):
    def __init__(self) -> None:
        self.globals = Environment()
        self.__env   = self.globals


    def interpreter(self, expressions: list[Stmt]) -> None:
        try:
            for expression in expressions:
                self.__evaluate(expression)
        except RuntimeError as error:
            print(f"{error.args[1]} at [line {str(error.args[0].line)}]")


    def __evaluate(self, expr: Expr|Stmt) -> object:
        return expr.accept(self)


    # overridee
    def visitReturnStmt(self, stmt: ReturnStmt) -> None:
        val = None
        if (stmt.val != None):
            val = self.__evaluate(stmt.val)
        raise Exception(val)

    # override
    def visitFuncStmt(self, stmt: FuncStmt) -> None:
        func = LoxFuntion(stmt, self.__env)
        self.__env.define(stmt.name.lexeme, func)
        return 

    # override
    def visitWhileStmt(self, stmt: WhileStmt) -> None:
        while (self.__evaluate(stmt.condition)):
            self.__evaluate(stmt.body)
        return 


    # override
    def visitLogicalExpr(self, expr: Logical):
        left = self.__evaluate(expr.left)
        if (expr.operator.type == TokenType.OR):
            if (left):  return left
        else:
            if (not left):  return left
        return self.__evaluate(expr.right)

    # override
    def visitIF(self, stmt: IF) -> None:
        if (self.__evaluate(stmt.condition)):
            self.__evaluate(stmt.thenBranch)
        elif (stmt.elseBranch != None):
            self.__evaluate(stmt.elseBranch)
        return

    # override
    def visitBlock(self, stmt: Block):
        self.executeBlock(stmt.statements, Environment(self.__env))
        return
    

    def executeBlock(self, stmts: list[Stmt], env: Environment) -> None:
        previous = self.__env

        try:
            self.__env = env
            for stmt in stmts:
                self.__evaluate(stmt)
        finally:
            self.__env = previous
        return
        

    # override
    def visitExprStm(self, stmt: ExprStmt) -> None:
        self.__evaluate(stmt.expr)
        return


    # override
    def visitPrintStmt(self, stmt: PrintStmt) -> None:
        val = self.__evaluate(stmt.expr)
        print(val)
        return


    # override
    def visitVarVarDecl(self, stmt: VarDecl) -> None:
        val = None
        if (stmt.indentifier != None):
            val = self.__evaluate(stmt.indentifier)

        self.__env.define(stmt.name.lexeme, val)
        return None


    # override
    def visitVariableExpr(self, expr: Variable) -> object:
        return self.__env.get(expr.name)

    
    # override
    def visitAssignExpr(self, expr: Assign) -> None:
        val = self.__evaluate(expr.val)
        self.__env.assign(expr.name, val)
        return


    # override
    def visitLiteralExpr(self, expr: Literal) -> object:
        return expr.val
    

    # override
    def visitGroupExpr(self, expr: Group) -> object:
        return self.__evaluate(expr.expression)
    

    # override
    def visitUnaryExpr(self, expr: Unary) -> object:
        right = self.__evaluate(expr.right)
        if (expr.operator.type == TokenType.MINUS):
            self.__checkNumberOperator(expr.operator, right)
            return -1 * right
        elif (expr.operator.type == TokenType.BANG):
            return not right
        else:
            raise "Unexpected operator in unary token" # how to handle error !!!
    

    # override
    def visitBinaryExpr(self, expr: Binary) -> object:
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
            
    
    # override
    def visitCallExpr(self, expr: Call) -> object:
        callee = self.__evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.__evaluate(argument))
        if (not isinstance(callee, LoxCallable)):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")
        if (len(arguments) != callee.arity()):
            raise RuntimeError(expr.paren, f"Expected {callee.arity()} arguments but got {len(arguments)}.")
        return  callee.call(self, arguments)



    def __checkNumberOperator(self, operator: Token, *operands: object) -> None:
        for op in operands:
            if (not isinstance(op, (float, int))):
                raise RuntimeError(operator, "Operand must be number")
        return
    
    
