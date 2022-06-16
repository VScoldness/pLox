class Lox:
    def __init__(self, input:str) -> None:
        self.hadError = False
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
            line = input("Please enter something: ")
            if (not line):
                break
            self.__run(line)
            self.hadError = False
        
    @staticmethod
    def __run(source:str) -> None:
        scanner = None
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token)
        return
    
    def error(self, line:int, message:str) -> None:
        self.__report(line, "", message)
        return

    def __report(self, line:int, where:str, message:str) -> None:
        print(f"[line {line} ] Error {where} : {message}")
        self.hadError = True
        return


        