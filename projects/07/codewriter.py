import os  
from pathlib import Path

class CodeWriter:
    def __init__(self,path):  #open the output file and get ready to write into it
        if os.path.isfile(path):
            filename = os.path.splitext(path)[0]  #get the file path without the extension
        else:
            filename = path #if it's a folder, don't need to get ride of extention
        self.basename = Path(path).stem #get the file basename without the extension
        self.name = f'{filename}.asm'
        self.comparison_count = 0
        with open(self.name, 'w+') : 
            pass
        
    def SetFileName(self,filepath):  #inform code writer that the translation of a new VM file is started
        self.basename = Path(filepath).stem #get the file basename without the extension
    
    def WriteArithmetic(self,command):
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
            label_n= f'label_{self.comparison_count}'
            self.comparison_count += 1 
            label_p= f'label_{self.comparison_count}'
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
                        

    def WritePushPop(self,command,segment,i):
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
                    
                


                



                




