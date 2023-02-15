from SymbolTable import *

class VMWriter:

    def __init__(self,output) :
        self.output = output
        with open(output, 'w+') : 
            pass

    def writePush(self,segment,index):
        with open(self.output, 'a+') as vm: 
            vm.write(f'push {segment} {index}\n')

    def writePop(self,segment,index):
        with open(self.output, 'a+') as vm: 
            vm.write(f'pop {segment} {index}\n')

    def writeArithmetic(self,command,unaryOp = 0):
        if command == '&':
            code = 'and\n'
        elif command == '|':
            code = 'or\n'
        elif command == '~':
            code = 'not\n'
        elif command == '=':
            code = 'eq\n'
        elif command == '>':
            code = 'gt\n'
        elif command == '<':
            code = 'lt\n'
        elif command == '+':
            code = 'add\n'
        elif command == '-':
            if unaryOp == 0:
                code = 'sub\n'
            elif unaryOp == 1:
                code = 'neg\n'
        with open(self.output, 'a+') as vm: 
            vm.write(code)
    
    def writeLabel(self,label):
        code = f'label {label}\n'
        with open(self.output, 'a+') as vm: 
            vm.write(code)

    def writeGoto(self,label):
        code = f'goto {label}\n'
        with open(self.output, 'a+') as vm: 
            vm.write(code)

    def writeIf(self,label):
        code = f'if-goto {label}\n'
        with open(self.output, 'a+') as vm: 
            vm.write(code)

    def writeCall(self,name, nArgs):
        code = f'call {name} {nArgs}\n'
        with open(self.output, 'a+') as vm: 
            vm.write(code)

    def writeFunction(self, name, nVars):
        code = f'function {name} {nVars}\n'
        with open(self.output, 'a+') as vm: 
            vm.write(code)
    
    def writeReturn(self):
        with open(self.output, 'a+') as vm: 
            vm.write('return\n')

