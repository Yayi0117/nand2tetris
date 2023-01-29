#Parser#
class Parser:
    def __init__(self, file):
        content=[]
        with open(file,mode='r') as f:
            lines=f.readlines()
        for line in lines:
            removed = line.replace(' ','')  #remove whitespace in conmmandlines
            if (removed is not None) and  (removed[0] != '/' ):  #exclude blank lines and comment lines.
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
                return None
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
                return None
        else:
            return None