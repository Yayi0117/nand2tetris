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