#Parser#
class Parser:
    def __init__(self, file):
        content=[]
        with open(file,mode='r') as f:
            lines=f.readlines()
        for line in lines:
            removed = line.replace(' ','')  #remove whitespace in conmmandlines
            if (removed != '\n') and  (removed[0] != '/' ):  #exclude blank lines and comment lines.
                removed = removed.replace('\n','')
                removed = removed.split('/')[0]
                content.append(removed)
        self.content = content
        self.current = 0    #initial current command is the 0th line

    def has_more_commands(self,current) : #check whether there are more commands after the current kth command?
        if current < len(self.content) :
            return True
        else:
            return False

    def advance(self,current):
        if self.has_more_commands(current):
            self.current += 1
    
    def commandType(self, current):
        if self.content[current][0] == '@' :
            return 'A_COMMAND'
        elif self.content[current][0] == '(':
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def symbol(self,current):
        if self.commandType(current) == 'A_COMMAND' :
            return self.content[current][1:]
        elif self.commandType(current) == 'L_COMMAND':
            return self.content[current][1:-1]
        else:
            return None

    def dest(self, current):
        if self.commandType(current) == 'C_COMMAND' :
            if '=' in self.content[current]:
                return self.content[current].split('=')[0]
            else:
                return ''
        else:
            return None
    
    def comp(self, current):
        if self.commandType(current) == 'C_COMMAND' :
            commandc = self.content[current]
            if '=' in commandc:
                rest = commandc.split('=')[1]
                if ';' in rest:
                    return rest.split(';')[0]
                else:
                    return rest
            else:
                if ';' in commandc:
                    return commandc.split(';')[0]
                else:
                    return commandc
        else:
            return None
    
    def jump(self, current):
        if self.commandType(current) == 'C_COMMAND' :
            if ';' in self.content[current]:
                return self.content[current].split(';')[1]
            else:
                return ''
        else:
            return None

#Code#
class Code:
    _dest_codes = {'':'000', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'} # The DEST part codes

    _comp_codes = {'0': '0101010', '1': '0111111', '-1':'0111010', 'D':'0001100', 'A': '0110000', '!D': '0001101',
                   '!A': '0110001', '-D': '0001111', '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
                   'D-1': '0001110', 'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D':'0000111',
                   'D&A': '0000000', 'D|A': '0010101', 'M': '1110000', '!M': '1110001', '-M': '1110011',
                   'M+1': '1110111', 'M-1': '1110010', 'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111',
                   'D&M': '1000000', 'D|M': '1010101'}      # The COMP part codes
    _jump_codes = {'':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}  # The JUMP part codes

    def __init__(self):
        pass

    def _bits(self, n):
        return bin(int(n))[2:]

    def gen_a_instruction(self, address_value):
        """
        Generates an A-Instruction from a specified address_value.
        :param address_value: Value of address in decimal.
        :return: A-Instruction in binary (String).
        """
        return '0' + self._bits(address_value).zfill(15)
    
    def gen_c_instruction(self, dest, comp, jump):
        """
        Generates an A-Instruction from a specified address_value.
        :param dest: 'dest' part of the instruction (string).
        :param comp: 'comp' part of the instruction (string).
        :param jump: 'jmp' part of the instruction (string).
        :return: C-Instruction in binary (string).
        """
        return '111' + self.comp(comp) + self.dest(dest) + self.jump(jump)
    
    def dest(self, d):
        """
        Generates the corresponding binary code for the given 'dest' instruction part.
        """
        return self._dest_codes[d]

    def comp(self, c):
        """
        Generates the corresponding binary code for the given 'comp' instruction part.
        """
        return self._comp_codes[c]

    def jump(self, j):
        """
        Generates the corresponding binary code for the given 'jmp' instruction part.
        """
        return self._jump_codes[j]

#SymbolTable#
class SymbolTable:
    """
    Implements a Symbol Table using a dictionary. The symbol
    table contains pre-defined values from the Hack machine specification
    and enables adding new keys for variables and label declarations.
    """
    def __init__(self):
        self.table = {
            'SP': 0, 'LCL': 1, 'ARG': 2, 'THIS': 3, 'THAT': 4,
            'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3, 'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
            'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11, 'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
            'SCREEN': 0x4000, 'KBD': 0x6000
        }

    def contains(self, symbol):
        """
        Checks if symbol table contains a given symbol
        """
        if symbol in self.table:
            return True
        else:
            return False

    def add_entry(self, symbol, address):
        self.table[symbol] = address

    def get_address(self, symbol):
        if self.contains(symbol):
            return self.table[symbol]
        else:
            return None

#main body#
inputfile = input('Please enter the file path you want to translate: ')
asm = Parser(inputfile)
code = Code()
symboltable = SymbolTable()
outputfile = 'program.hack'
i=16
k=0
total = 0

while k < len(asm.content):            #first pass
    line = asm.content[k]
    type = asm.commandType(k)
    if type == 'L_COMMAND':
        symbol = line[1:-1]
        symboltable.add_entry(symbol,total)
    else:
        total += 1
    k += 1

result = ''
m=0
while m < len(asm.content):            #second pass
    line = asm.content[m]
    type = asm.commandType(m)
    if type == 'L_COMMAND':
        m += 1
    elif type == 'A_COMMAND':
        tail = line[1:]
        if not tail.isdigit():
            if symboltable.contains(tail) == False:
                 symboltable.add_entry(tail,i)
                 i += 1
            tail = symboltable.get_address(tail)
        translated = code.gen_a_instruction(tail)
        m += 1
        result += translated + '\n'
        #with open(outputfile, 'w+') as file_object: 
        #    file_object.write(translated)
    elif type == 'C_COMMAND':
        d = asm.dest(m)
        c = asm.comp(m)
        j = asm.jump(m)
        translated = code.gen_c_instruction(d, c, j)
        m +=1
        result += translated + '\n'

with open(outputfile, 'w+') as file_object: 
    file_object.write(result.rstrip())
