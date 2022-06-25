from ErrorHandler import *
from TokenType import *
from Token import *


class Scanner():
    def __init__(self, source:str) -> None:
        self.source     = source
        self.tokens     = []
        self.__start    = 0
        self.__current  = 0
        self.__line     = 1
        self.__kws      = self.__buildKeyWord()
    

    @staticmethod
    def __buildKeyWord() -> dict():
        keywords = {}
        keywords['and']     = TokenType.AND
        keywords['class']   = TokenType.CLASS
        keywords['else']    = TokenType.ELSE
        keywords['for']     = TokenType.FOR
        keywords['fun']     = TokenType.FUN
        keywords['if']      = TokenType.IF
        keywords['nil']     = TokenType.NIL
        keywords['or']      = TokenType.OR
        keywords['print']   = TokenType.PRINT
        keywords['return']  = TokenType.RETURN
        keywords['super']   = TokenType.SUPER
        keywords['this']    = TokenType.THIS
        keywords['true']    = TokenType.TRUE
        keywords['var']     = TokenType.VAR
        keywords['while']   = TokenType.WHILE
        return keywords
        

    # scan the whole given source input
    def scanTokens(self) -> list[Token]:
        while (not self.__isAtEnd()):
            self.__start = self.__current
            self.__scanToken()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.__line))
        return self.tokens
    
    
    def __isAtEnd(self) -> bool:
        return self.__current >= len(self.source)
    

    def __scanToken(self) -> None:
        c = self.__advance() # !!!
        match c:
            case "(": self.__addToken(TokenType.LEFT_PAREN)
            case ')': self.__addToken(TokenType.RIGHT_PAREN)
            case '{': self.__addToken(TokenType.LEFT_BRACE)
            case '}': self.__addToken(TokenType.RIGHT_BRACE)
            case ',': self.__addToken(TokenType.COMMA)
            case '.': self.__addToken(TokenType.DOT)
            case '-': self.__addToken(TokenType.MINUS)
            case '+': self.__addToken(TokenType.PLUS)
            case ';': self.__addToken(TokenType.SEMICOLON)
            case '*': self.__addToken(TokenType.STAR)
            case "!": self.__addToken(TokenType.BANG_EQUAL)     if (self.__match("=")) else self.__addToken(TokenType.BANG)
            case "=": self.__addToken(TokenType.EQUAL_EQUAL)    if (self.__match("=")) else self.__addToken(TokenType.EQUAL)
            case "<": self.__addToken(TokenType.LESS_EQUAL)     if (self.__match("=")) else self.__addToken(TokenType.LESS)
            case ">": self.__addToken(TokenType.GREATER_EQUAL)  if (self.__match("=")) else self.__addToken(TokenType.GREATER)
            case "/": self.__findComment()                      if (self.__match("/")) else self.__addToken(TokenType.SLASH)
            case " ": " "       # empty string to skip the match-case statement
            case "\r": " "      # empty string to skip the match-case statement
            case "\t": " "      # empty string to skip the match-case statement
            case "\n": self.__line += 1
            case '"' : self.__string() 
            case _:
                if (c.isdigit()):
                    self.__number()
                elif (c.isalpha() or c == '_'):
                    self.__indentifier()
                else:
                    ErrorHandler.error(self.__line, "Unexpected character.")


    def __indentifier(self) -> None:
        while (self.__isAlphaNumericUnderscore(self.__peek())):
            self.__advance()
        text = self.source[self.__start:self.__current]
        type = self.__kws.get(text)
        if (not type):
            type = TokenType.IDENTIFIER
        self.__addToken(type)


    @staticmethod
    def __isAlphaNumericUnderscore(c:str):
        return c.isalpha() or c.isdigit() or c == '_'


    # find number in the script and save it into tokens
    def __number(self) -> None:
        while (self.__peek().isdigit()):
            self.__advance()
        if (self.__peek() == "." and self.__peekNext().isdigit()):
            self.__advance()
            while (self.__peek().isdigit()):
                self.__advance()
        self.__addToken(TokenType.NUMBER, float(self.source[self.__start : self.__current]))


    def __peekNext(self) -> str:
        if (self.__current+1 >= len(self.source)):
            return '\0'
        return self.source[self.__current+1]


    # find string in the script and save it into tokens
    def __string(self) -> None:
        while (self.__peek() != '"' and not self.__isAtEnd()):
            if (self.__peek() == '\n'):
                self.__line += 1
            self.__advance()
        if (self.__isAtEnd()):
            ErrorHandler.error(self.__line, "Unterminated String")
            return
        self.__advance()
        string = self.source[self.__start+1 : self.__current-1]
        self.__addToken(TokenType.STRING, string)


    # remove the comments in the given script
    def __findComment(self) -> None:
        while (self.__peek() != '\n' and not self.__isAtEnd()):
            self.__advance()


    def __peek(self) -> str:
        if (self.__isAtEnd()):
            return '\0'
        return self.source[self.__current]


    # according to next char to determine the token type (e.g. <= or <)
    def __match(self, expected:str) -> bool:
        if (self.__isAtEnd()):
            return False
        if (self.source[self.__current] != expected):
            return False
        self.__current += 1
        return True


    def __advance(self) -> str:
        self.__current += 1
        return self.source[self.__current-1]
    

    def __addToken(self, type:TokenType, literal = None) -> None:
        text = self.source[self.__start : self.__current]
        self.tokens.append(Token(type, text, literal, self.__line))

    
