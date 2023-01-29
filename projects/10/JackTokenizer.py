import xml.etree.cElementTree as ET
import re

class JackTokenizer:
    keywords = ['class', 'constructor', 'function', 
		'method', 'field', 'static', 'var', 'int', 'char',
		'boolean', 'void', 'true', 'false', 'null', 'this',
		'let', 'do', 'if', 'else', 'while', 'return']
    symbols = ['{', '}', '(', ')', '[', ']', '.',',',
		 ';', '+', '-', '*', '/', '&', '|', '<', '>','=', '~']

    def __init__(self,file):
        tokens=[]
        with open(file,mode='r') as f:
            lines=f.readlines()
        for line in lines:
            line = line.strip() #get rid of leading and tailing whitespaces in lines
            if len(line)>0 and (line[0] not in ['\n','/','*']):  #exclude blank lines and comment lines
                line = line.replace('\n','') #get rid of \n in lines
                line = line.split('//')[0] #get rid of comment in lines
                sublines = line.split('"')  # pick out the stringConstant
                for i in range(len(sublines)):
                    if i%2 == 0: #when the subline is not stringConstant, generate tokens from it
                        sublines[i]=[token for token in re.split('(\W)',sublines[i]) if token not in ('', ' ')] 
                        tokens.extend(sublines[i])
                    if i%2 == 1: #when the subline is a stringConstant, put a pair of " around it 
                        sublines[i]='"'+sublines[i]+'"'
                        tokens.append(sublines[i]) #append the subline as a token into the tokens' set
        self.tokens = tokens # pass all generated tokens to self.tokens
        
    def hasMoreTokens(self):
        if len(self.tokens) > 0:
            return True
        else:
            return False
    
    def advance(self):
        self.current_token = self.tokens.pop(0)

    def tokenType(self):
        if self.current_token in JackTokenizer.keywords:
            return 'KEYWORD'
        elif self.current_token in JackTokenizer.symbols:
            return 'SYMBOL'
        elif self.current_token.isdigit():
            return 'INT_CONST'
        elif self.current_token[0] == '"':  
            return 'STRING_CONST'
        else:
            return 'IDENTIFIER'        

    def keyWord(self):
        return self.current_token

    def symbol(self):
        return self.current_token

    def identifier(self):
        return self.current_token

    def intVal(self):
        return int(self.current_token)

    def stringVal(self):
        return self.current_token[1:-1]



#the following code is used to test JackTokenizer:

file = input("enter the file path you want to tokenize: ")
tokenizer = JackTokenizer(file)
root = ET.Element('tokens')  # generate file root 'tokens'
root.text = '\n'
root.tail = '\n'
while tokenizer.hasMoreTokens():  #generate subtrees
    tokenizer.advance()
    if tokenizer.tokenType() == 'KEYWORD':
        newElement = ET.SubElement(root, "keyword")
        newElement.text = ' '+tokenizer.keyWord()+' '
        newElement.tail = '\n'
    elif tokenizer.tokenType() == 'SYMBOL':
        newElement = ET.SubElement(root, "symbol")
        newElement.text = ' '+tokenizer.symbol()+' '
        newElement.tail = '\n'
    elif tokenizer.tokenType() == 'IDENTIFIER':
        newElement = ET.SubElement(root, "identifier")
        newElement.text = ' '+tokenizer.identifier()+' '
        newElement.tail = '\n'
    elif tokenizer.tokenType() == 'INT_CONST':
        newElement = ET.SubElement(root, "integerConstant")
        newElement.text = ' '+str(tokenizer.intVal())+' '
        newElement.tail = '\n'
    elif tokenizer.tokenType() == 'STRING_CONST':
        newElement = ET.SubElement(root, "stringConstant")
        newElement.text = ' '+str(tokenizer.stringVal())+' '
        newElement.tail = '\n'

tree = ET.ElementTree(root)
tree.write((file[:-5]+'TT.xml')) # write off the whole tree
    


