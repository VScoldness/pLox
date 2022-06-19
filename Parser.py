from typing import TYPE_CHECKING

from Expr import *
if TYPE_CHECKING:
    from Lox import *

class ParserError(RuntimeError):
    pass

class Parser:
    def __init__(self, tokens: list[Token]) -> None:
        self.__tokens = tokens
        self.__current = 0
    

    def parse(self) -> Expr:
        try:
            return self.__expression()
        except:
            print("Error Happen")
            return
    

    def __expression(self) -> Expr:
        return self.__equality()
    

    def __equality(self) -> Expr:
        expr = self.__comparsion()

        while (self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            operator = self.__previous()
            right = self.__comparsion()
            expr = Binary(expr, operator, right)
        
        return expr
    

    def __comparsion(self) -> Expr:
        expr = self.__term()

        while (self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)):
            operator = self.__previous()
            right = self.__term()
            expr = Binary(expr, operator, right)
        
        return expr

    
    def __term(self) -> Expr:
        expr = self.__factor()

        while (self.__match(TokenType.PLUS, TokenType.MINUS)):
            operator = self.__previous()
            right = self.__factor()
            expr = Binary(expr, operator, right)
        
        return expr
    

    def __factor(self) -> Expr:
        expr = self.__unary()

        while (self.__match(TokenType.STAR, TokenType.SLASH)):
            operator = self.__previous()
            right = self.__unary()
            expr = Binary(expr, operator, right)
        
        return expr
    

    def __unary(self) -> Expr:
        
        if (self.__match(TokenType.MINUS, TokenType.BANG)):
            operator = self.__previous()
            right = self.__unary()
            expr = Unary(operator, right)
            return expr

        return self.__primary()
    

    def __primary(self) -> Expr:
        if (self.__match(TokenType.FALSE)):                     return Literal(False)
        if (self.__match(TokenType.TRUE)):                      return Literal(True)
        if (self.__match(TokenType.NIL)):                       return Literal(None)
        if (self.__match(TokenType.NUMBER, TokenType.STRING)):  return Literal(self.__previous().literal)
        if (self.__match(TokenType.LEFT_PAREN)):                return self.__group()

        raise self.__error(self.__peek(), "Expect expression.")

    def __group(self) -> Expr:
        expr = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
        return Group(expr)


    def __match(self, *argv: TokenType) -> bool:
        for arg in argv:
            if (self.__check(arg)):
                self.__advance()
                return True
        return False
    

    def __check(self, type: TokenType) -> bool:
        if (self.__isAtEnd()):  return False
        return self.__peek().type == type
    

    def __advance(self) ->Token:
        if (not self.__isAtEnd()):  self.__current += 1
        return self.__previous()
    

    def __isAtEnd(self) -> bool:
        return self.__peek().type == TokenType.EOF
    

    def __peek(self) -> Token:
        return self.__tokens[self.__current]
    

    def __previous(self) -> Token:
        return self.__tokens[self.__current-1]
    

    def __consume(self, type: TokenType, message: str) -> Token:
        if (self.__check(type)):    return self.__advance()
        raise self.__error(self.__peek(), message)
    

    def __error(self, token: Token, message: str) -> ParserError:
        Lox.error(token, message)
        return ParserError()
    

    def __synchronize(self) -> None:
        token = self.__advance()

        while (not self.__isAtEnd()):
            if (token.type == TokenType.EOF):   return

            match self.__peek().type:
                case TokenType.CLASS:   return
                case TokenType.FUN:     return
                case TokenType.VAR:     return
                case TokenType.FOR:     return
                case TokenType.IF:      return
                case TokenType.WHILE:   return
                case TokenType.PRINT:   return
                case TokenType.RETURN:  return
            
            token = self.__advance()

