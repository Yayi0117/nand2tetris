class Parse:
    arithm = 'C_ARITHMETIC'
    push = 'C_PUSH'
    pop = 'C_POP'
    label = 'C_LABEL'
    goto = 'C_GOTO'
    con = 'C_IF'
    func = 'C_FUNCTION'
    re = 'C_RETURN'
    call = 'C_CALL'

    def __init__(self, file):
        content=[]
        with open(file,mode='r') as f:
            lines=f.readlines()
        for line in lines:
            if (line != '\n') and  (line[0] != '/' ):  #exclude blank lines and comment lines.
                line = line.replace('\n','') #get rid of \n
                line = line.split('/')[0]  #get rid of comment
                line = line.strip() #get rid of any leading and trailing spaces for each VM command
                line = line.split(' ')
                content.append(line)
        self.content = content
        self.current = 0    #initial current command is the 0th line
        
    def has_more_commands(self) : #check whether there are more commands after the current kth command?
        if self.current < len(self.content) :
            return True
        else:
            return False

    def advance(self):
        self.current += 1

    def commandType(self, current):
        if len(self.content[current]) == 1 and self.content[current][0] != "return":
            return Parse.arithm
        elif self.content[current][0] == "push" :
            return Parse.push
        elif self.content[current][0] == "pop" :
            return Parse.pop
        elif self.content[current][0] == "label":
            return Parse.label
        elif self.content[current][0] == "goto":
            return Parse.goto
        elif self.content[current][0] == "if-goto":
            return Parse.con
        elif self.content[current][0] == "function":
            return Parse.func
        elif self.content[current][0] == "call":
            return Parse.call
        elif self.content[current][0] == "return":
            return Parse.re
    
    def arg1(self, current):
        if self.commandType(current)==Parse.arithm:
            return self.content[current][0]
        elif self.commandType(current)==Parse.push or self.commandType(current)==Parse.pop:
            return self.content[current][1]

    def arg2(self, current):
        return self.content[current][2]

