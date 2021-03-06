from Scanner import *
# from Parser import *
from AstPrinter import *
from ErrorHandler import *
from Interpreter import *
from Resolver import *

class Lox:
    def __init__(self, input=None) -> None:
        self.ErrorHandler = ErrorHandler()
        self.interpreter  = Interpreter()
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
        # if (self.ErrorHandler.hadError):
        #     return
    

    # run Lox from command line
    def __runPrompt(self) -> None:
        while True:
            line = input(">  ")
            if (not line):
                break
            self.__run(line)
            # self.ErrorHandler.hadError = False
        

    def __run(self, source:str) -> None:
        scanner = Scanner(source)
        tokens = scanner.scanTokens()
        parser = Parser(tokens)
        statements = parser.parse()

        if (self.ErrorHandler.hadError):
            return

        # for token in tokens:
        #     token.toString()

        # for stmt in statements:
            # print(stmt)
            # print(stmt.body)
            # print(stmt.body.statements)
        
        resolver = Resolver(self.interpreter)
        resolver.resolve(statements)

        self.interpreter.interpreter(statements)
        


        # print(AstPrinter().out(expression))


input = ["test/function_test.txt"]
Lox(input)