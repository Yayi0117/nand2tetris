import os  
from pathlib import Path

class CodeWriter:
    def __init__(self,path):  #open the output file and get ready to write into it
        self.basename = Path(path).stem #get the file basename without the extension
        if os.path.isfile(path):
            filename = os.path.splitext(path)[0]  #get the file path without the extension
        else:
            filename = path+f'/{self.basename}' #if it's a folder, don't need to get ride of extention,but add the output file in the folder
        self.name = f'{filename}.asm'
        self.comparison_count = 0
        self.funccall_count = 0
        with open(self.name, 'w+') : 
            pass
        
    def SetFileName(self,filepath):  #inform code writer that the translation of a new VM file is started
        self.basename = Path(filepath).stem #get the file basename without the extension
    
    def writeArithmetic(self,command):
        fullcommand = []
        if command[0] in ['add','sub','and','or']:
            prefix = ['@SP\n','M=M-1\n','A=M-1\n','D=M\n','@SP\n','A=M\n']
            suffix = ['@SP\n','A=M-1\n','M=D\n']
            if command[0] == 'add':
                operator = ['D=M+D\n']
            elif command[0] == 'sub':
                operator = ['D=D-M\n']
            elif command[0] == 'and':
                operator = ['D=M&D\n']
            elif command[0] == 'or':
                operator = ['D=M|D\n']
            fullcommand = prefix+operator+suffix
        elif command[0] in ['neg','not']:
            prefix = ['@SP\n','A=M-1\n']
            if command[0] == 'neg':
                operator = ['M=-M\n']
            elif command[0] == 'not':
                operator = ['M=!M\n']
            fullcommand = prefix+operator
        elif command[0] in ['eq','lt','gt']:
            label_n= f'label_{self.comparison_count}'    #generate a unique label for jumption if the value is negetive 
            self.comparison_count += 1 
            label_p= f'label_{self.comparison_count}'     #generate a unique label for jumption if the value is positive
            self.comparison_count += 1 
            label_end= f'endlabel_{self.comparison_count}'
            self.comparison_count += 1 
            prefix = ['@SP\n','M=M-1\n','A=M-1\n','D=M\n''@SP\n','A=M\n','D=D-M\n']
            suffix = [f'({label_n})\n','@SP\n','A=M-1\n','M=0\n',f'@{label_end}\n','0;JMP\n',f'({label_p})\n','@SP\n','A=M-1\n''M=-1\n',f'({label_end})\n']
            if command[0] == 'eq':
                logic_n = [f'@{label_n}\n','D;JNE\n']
                logic_p = [f'@{label_p}\n','D;JEQ\n']
            elif command[0] == 'gt':
                logic_n = [f'@{label_n}\n','D;JLE\n']
                logic_p = [f'@{label_p}\n','D;JGT\n']
            elif command[0] == 'lt':
                logic_n = [f'@{label_n}\n','D;JGE\n']
                logic_p = [f'@{label_p}\n','D;JLT\n']
            fullcommand = prefix+logic_p+logic_n+suffix
        comment = ' '.join(command)
        writedown = ''.join(fullcommand)
        with open(self.name, 'a+') as asm: 
            asm.write(f'// translate: {comment}\n')
            asm.write(writedown)      
                        

    def writePushPop(self,command,segment,i):
        if command[0] == 'push':
            if segment in ['local','argument','this','that']:
                if segment == 'local':
                    defult = 'LCL'
                elif segment == 'argument':
                    defult = 'ARG'
                elif segment == 'this':
                    defult = 'THIS'                        
                elif segment == 'that':
                    defult = 'THAT'
                fullcommand = [f'@{defult}\n','D=M\n',f'@{i}\n','A=D+A\n','D=M\n','@SP\n','A=M\n','M=D\n','@SP\n','M=M+1\n']                    
            elif segment in ['pointer','temp']:
                if segment == 'pointer':
                    defult = '3'
                elif segment == 'temp':
                    defult = '5'
                fullcommand = [f'@{defult}\n','D=A\n',f'@{i}\n','A=D+A\n','D=M\n','@SP\n','A=M\n','M=D\n','@SP\n','M=M+1\n']
            elif segment == 'static':
                fullcommand = [f'@{self.basename}.{i}\n','D=M\n','@SP\n','A=M\n','M=D\n','@SP\n','M=M+1\n']
            elif segment == 'constant':
                fullcommand = [f'@{i}\n','D=A\n','@SP\n','A=M\n','M=D\n','@SP\n','M=M+1\n']                                
        elif command[0] == 'pop':
            if segment in ['local','argument','this','that']:
                if segment == 'local':
                    defult = 'LCL'
                elif segment == 'argument':
                    defult = 'ARG'
                elif segment == 'this':
                    defult = 'THIS'                        
                elif segment == 'that':
                    defult = 'THAT'
                fullcommand = [f'@{defult}\n','D=M\n',f'@{i}\n','D=D+A\n','@R13\n','M=D\n','@SP\n','M=M-1\n','A=M\n','D=M\n','@R13\n','A=M\n','M=D\n']                    
            elif segment in ['pointer','temp']:
                if segment == 'pointer':
                    defult = '3'
                elif segment == 'temp':
                    defult = '5'
                fullcommand = [f'@{i}\n','D=A\n',f'@{defult}\n','D=A+D\n','@R13\n','M=D\n','@SP\n','M=M-1\n','A=M\n','D=M\n','@R13\n','A=M\n','M=D\n']
            elif segment == 'static':
                fullcommand = ['@SP\n','M=M-1\n','A=M\n','D=M\n',f'@{self.basename}.{i}\n','M=D\n']
        comment = ' '.join(command)
        writedown = ''.join(fullcommand)
        with open(self.name, 'a+') as asm: 
            asm.write(f'// translate: {comment}\n')
            asm.write(writedown)      
                    
    def writeInite(self):
        """
        translate the following commands into assembly code:
        SP=256
        call Sys.init 0
        """
        fullcommand = ['@256','D=A','@SP','M=D']  
        fullcommand +=['@BOOTSTRAP','D=A','@SP','A=M','M=D']  #push retaddr 'BOOTSTRAP'
        for segment in ["LCL","ARG","THIS","THAT"]: #push current "LCL","ARG","THIS","THAT"
            fullcommand +=[f'@{segment}','D=M','@SP','M=M+1','A=M','M=D']
        fullcommand +=['@SP','M=M+1'] #advance SP by one
        fullcommand +=['@5','D=A','@SP','D=M-D','@ARG','M=D'] #ARG=SP-5
        fullcommand +=['@SP','D=M','@LCL','M=D'] #LCL=SP
        fullcommand +=['@Sys.init','0;JMP','(BOOTSTRAP)']
        with open(self.name, 'a+') as asm: 
            for line in fullcommand:
                asm.write(f'{line}\n')
    
    def writeLabel(self,label):
        label = self.basename+'.'+label
        with open(self.name, 'a+') as asm: 
            asm.write(f'({label})\n')

    def writeGoto(self,label):
        label = self.basename+'.'+label
        fullcommand = [f'@{label}','0;JMP']
        with open(self.name, 'a+') as asm: 
            for line in fullcommand:
                asm.write(f'{line}\n')

    def writeIf(self,label):
        label = self.basename+'.'+label
        fullcommand = ['@SP','M=M-1','A=M','D=M',f'@{label}','D;JNE']
        with open(self.name, 'a+') as asm: 
            for line in fullcommand:
                asm.write(f'{line}\n')

    def writeCall(self,functionName,numArgs):
        retAddr = functionName+'.$ret.'+ str(self.funccall_count) #creat the return address label for this call
        fullcommand = [f'@{retAddr}','D=A','@SP','A=M','M=D']  #push retaddress
        self.funccall_count +=1 #increase by one eveytime the program call a function
        for segment in ["LCL","ARG","THIS","THAT"]: #push current "LCL","ARG","THIS","THAT"
            fullcommand +=[f'@{segment}','D=M','@SP','M=M+1','A=M','M=D']
        fullcommand +=['@SP','M=M+1'] #advance SP by one
        fullcommand +=[f'@{numArgs}','D=A','@5','D=A+D','@SP','D=M-D','@ARG','M=D'] #ARG=SP-n-5
        fullcommand +=['@SP','D=M','@LCL','M=D'] #LCL=SP
        fullcommand +=[f'@{functionName}','0;JMP',f'({retAddr})']
        with open(self.name, 'a+') as asm: 
            for line in fullcommand:
                asm.write(f'{line}\n')
    
    def writeFunction(self,functionName,numLocals):
        fullcommand = [f'({functionName})']
        for i in range(int(numLocals)):
            fullcommand += ['@SP','A=M','M=0','@SP','M=M+1']
        with open(self.name, 'a+') as asm: 
            for line in fullcommand:
                asm.write(f'{line}\n')

    def writeReturn(self):
        fullcommand =["@LCL","D=M","@R15","M=D"] # put LCL into R15
        fullcommand +=["@5","D=A","@R15","A=M-D","D=M","@R14","M=D"] # put retAddr into R14
        fullcommand +=["@SP","AM=M-1","D=M","@ARG","A=M","M=D"] # *ARG=pop()
        fullcommand +=["@ARG","D=M+1","@SP","M=D"] # SP=ARG+1
        fullcommand +=["@R15","A=M-1","D=M","@THAT","M=D"] # THAT=*(FRAME-1)
        fullcommand +=["@2","D=A","@R15","A=M-D","D=M","@THIS","M=D"] #THIS=*(FRAME-2)
        fullcommand +=["@3","D=A","@R15","A=M-D","D=M","@ARG","M=D"] # ARG=*(FRAME-3)
        fullcommand +=["@4","D=A","@R15","A=M-D","D=M","@LCL","M=D"] # LCL=*(FRAME-4)
        fullcommand +=["@R14","A=M","0;JMP"] # goto retAddr
        with open(self.name, 'a+') as asm: 
            for line in fullcommand:
                asm.write(f'{line}\n')

    

    
    


                



                



                




