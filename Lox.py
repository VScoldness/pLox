from Scanner import *
from Parser import *
from AstPrinter import *

class Lox:
    def __init__(self, input=None) -> None:
        self.hadError = False
        if (not input):
            self.__runPrompt()
        if (len(input) > 1):
            print("Invalid Input, please specify a Lox script or run it in command line (empty input)")
            return
        elif (len(input) == 1):
            self.__runFile(input[0])
        else:
            self.__runPrompt()

    # run Lox from script
    def __runFile(self, input:str) -> None:
        file = open(input, 'r')
        loxInput = file.read()
        self.__run(loxInput)
        if (self.hadError):
            return
    
    # run Lox from command line
    def __runPrompt(self) -> None:
        while True:
            line = input(">  ")
            if (not line):
                break
            self.__run(line)
            self.hadError = False
        
    def __run(self, source:str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        expression = parser.parse()

        if (self.hadError):
            return

        # for token in tokens:
        #     token.toString()
        # return

        # print(expression)

        print(AstPrinter().out(expression))

    
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

Lox()