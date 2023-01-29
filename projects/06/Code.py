#Code#
class Code:
    _dest_codes = {'':'001', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'} # The DEST part codes

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