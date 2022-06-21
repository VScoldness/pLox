import Token
import TokenType

class ErrorHandler:
    def __init__(self) -> None:
        self.hadError = False
    

    def error(self, line:int, message:str) -> None:
        self.__report(line, "", message)
        return
    

    def parserError(self, token: Token, message: str) -> None:
        if (token.type == TokenType.EOF):
            self.__report(token.line, " at end", message)
        return self.__report(token.line, " at '{}'".format(token.lexeme), message)


    def __report(self, line:int, where:str, message:str) -> None:
        print(f"[line {line} ] Error {where} : {message}")
        self.hadError = True
        return