from Parser import *
import enum

class FunctionType(enum.Enum):
    # Single-character tokens.
    NONE            = 1
    FUNCTION        = 2

class Resolver(Visitor, VisitorStmt):
    def __init__(self, interpreter) -> None:
        self.interpreter = interpreter
        self.scopes = []
        self.__currentFunction = FunctionType.NONE

    def resolve(self, stmts: list[Stmt]) -> None:
        for stmt in stmts:
            self.__resolve(stmt)
    

    def __resolve(self, stmt: Stmt|Expr) -> None:
        stmt.accept(self)


    # override
    def visitBlock(self, stmt: Block) -> None:
        self.__beginScope()
        self.resolve(stmt.statements)
        self.__endScope()
        return
    

    def __beginScope(self) -> None:
        self.scopes.append({})
    

    def __endScope(self) -> None:
        self.scopes.pop()
    

    #override
    def visitVarVarDecl(self, stmt: VarDecl) -> None:
        self.__declare(stmt.name)
        if (stmt.indentifier != None):
            self.__resolve(stmt.indentifier)
        self.__define(stmt.name)
        return


    def __declare(self, name: Token) -> None:
        if (len(self.scopes) == 0):
            return
        scope = self.scopes[-1]
        if (name.lexeme in scope):
            ErrorHandler().error(name, "Variable with this name already in this scope.")
        scope[name.lexeme] = False
    

    def __define(self, name: Token) -> None:
        if (len(self.scopes) == 0):
            return
        scope = self.scopes[-1]
        scope[name.lexeme] = True
    

    #override
    def visitVariableExpr(self, expr: Variable) -> None:
        if (len(self.scopes) != 0) and (self.scopes[-1].get(expr.name.lexeme) == False):
            raise "Can't read local variable in its own initializer."
        self.__resolveLocal(expr, expr.name)
        return
    

    def __resolveLocal(self, expr: Expr, name: Token) -> None:
        for idx in range(len(self.scopes)-1, -1, -1):
            if (name.lexeme in self.scopes[idx]):
                self.interpreter.resolve(expr, len(self.scopes)-1-idx)
                return
        

    #override
    def visitAssignExpr(self, expr: Assign) -> None:
        self.__resolve(expr.val)
        self.__resolveLocal(expr, expr.name)
        return
    
    #override
    def visitFuncStmt(self, stmt: FuncStmt) -> None:
        self.__declare(stmt.name)
        self.__define(stmt.name)
        self.__resolveFunc(stmt, FunctionType.FUNCTION)
    

    def __resolveFunc(self, func: FuncStmt, type: FunctionType) -> None:
        enclosingFunction = self.__currentFunction
        self.__currentFunction = type
        self.__beginScope()
        for param in func.params:
            self.__declare(param)
            self.__define(param)
        self.resolve(func.body)
        self.__endScope()
        self.__currentFunction = enclosingFunction
    

    #override
    def visitExprStm(self, stmt: ExprStmt) -> None:
        self.__resolve(stmt.expr)
        return
    

    #override
    def visitIF(self, stmt: IF) -> None:
        self.__resolve(stmt.condition)
        self.__resolve(stmt.thenBranch)
        if (stmt.elseBranch):
            self.__resolve(stmt.elseBranch)
        return

    
    #override
    def visitPrintStmt(self, stmt: PrintStmt) -> None:
        self.__resolve(stmt.expr)
        return
    

    #override
    def visitReturnStmt(self, stmt: ReturnStmt) -> None:
        if (self.__currentFunction == FunctionType.NONE):
            ErrorHandler().error(stmt.keyword, "Variable with this name already in this scope.")
        if (stmt.val != None):
            self.__resolve(stmt.val)
        return


    #override
    def visitWhileStmt(self, stmt: WhileStmt) -> None:
        self.__resolve(stmt.condition)
        self.__resolve(stmt.body)
        return
    

    #override
    def visitBinaryExpr(self, expr: Binary) -> None:
        self.__resolve(expr.left)
        self.__resolve(expr.right)
        return
    

    #override
    def visitCallExpr(self, expr: Call) -> None:
        self.__resolve(expr.callee)
        for arg in expr.arguments:
            self.__resolve(arg)
        return
    

    #override
    def visitGroupExpr(self, expr: Group) -> None:
        self.__resolve(expr.expression)
        return
    

    #override
    def visitLiteralExpr(self, expr: Literal) -> None:
        return
    

    #override
    def visitLogicalExpr(self, expr: Logical):
        self.__resolve(expr.left)
        self.__resolve(expr.right)
        return
    

    #override
    def visitUnaryExpr(self, expr: Unary):
        self.__resolve(expr.right)
        return
    

    

