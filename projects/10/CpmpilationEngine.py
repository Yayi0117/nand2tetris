from JackTokenizer import *
import xml.etree.cElementTree as ET

class CompilationEngine:
    terminals = {'keyword':'KEYWORD','symbol':'SYMBOL','identifier':'IDENTIFIER','integerConstant':'INT_CONST','stringConstant':'STRING_CONST'}

    def __init__(self,input,output):
        self.tokenizer = input
        self.output = output

    def process(self,root,terminaltype):
        """
        A helper method that handles 
        the current token, and advances
        to get the next token.

        if (currentToken in str)
            printXMLToken(str)
        else
            print("syntax error")
        currentToken = tokenizer.advance()
        """
        current_type = self.tokenizer.tokenType()
        if current_type != self.terminals[terminaltype]:
            newElement = ET.SubElement(root, f"not{terminaltype}")
            newElement.text = ' '+self.tokenizer.current_token+' '
            newElement.tail = '\n'
        else:
            if current_type == 'KEYWORD':
                newElement = ET.SubElement(root, "keyword")
                newElement.text = ' '+self.tokenizer.keyWord()+' '
                newElement.tail = '\n'
            elif current_type == 'SYMBOL':
                newElement = ET.SubElement(root, "symbol")
                newElement.text = ' '+self.tokenizer.symbol()+' '
                newElement.tail = '\n'
            elif current_type == 'IDENTIFIER':
                newElement = ET.SubElement(root, "identifier")
                newElement.text = ' '+self.tokenizer.identifier()+' '
                newElement.tail = '\n'
            elif current_type == 'INT_CONST':
                newElement = ET.SubElement(root, "integerConstant")
                newElement.text = ' '+str(self.tokenizer.intVal())+' '
                newElement.tail = '\n'
            elif current_type == 'STRING_CONST':
                newElement = ET.SubElement(root, "stringConstant")
                newElement.text = ' '+self.tokenizer.stringVal()+' '
                newElement.tail = '\n' 
        self.tokenizer.advance()     


    def compileClass(self):
        #class: 'class'className '{'classVarDec* subroutineDec*'}'
        root = ET.Element('class')  # generate file root 'class'
        root.text = '\n'
        root.tail = '\n'
        self.tokenizer.advance()  #first advance
        self.process(root,'keyword') #'class'
        self.process(root,'identifier') #classname
        self.process(root,'symbol') #'{'
        while self.tokenizer.current_token in ['field', 'static']:  #classVarDec*
            self.compileClassVarDec(root)
        while self.tokenizer.current_token in ['constructor','function','method']:  #subroutineDec*
            self.compileSubroutine(root)
        # the last symbol
        newElement = ET.SubElement(root, "symbol")
        newElement.text = ' } '
        newElement.tail = '\n' 

        tree = ET.ElementTree(root)
        tree.write(self.output)   # write off the whole tree

    def compileClassVarDec(self,root):
        # classVarDec: ('field'|'static') type varName (','varName)*';'
        newroot = ET.SubElement(root, 'classVarDec')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.process(newroot,'keyword') #'field'|'static'
        if self.tokenizer.tokenType() == 'KEYWORD': #type
            self.process(newroot,'keyword')
        else:
            self.process(newroot,'identifier')
        self.process(newroot,'identifier') #varName
        while self.tokenizer.current_token != ';': #(','varName)*
            self.process(newroot,'symbol') 
            self.process(newroot,'identifier')
        self.process(newroot,'symbol') #';'         

    def compileSubroutine(self,root):
        #subroutineDec: ('constructor'|'function'|'method')('void'|type)subroutineName'('parameterList')'subroutineBody
        newroot = ET.SubElement(root, 'subroutineDec')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.process(newroot,'keyword')#'constructor'|'function'|'method'
        if self.tokenizer.tokenType() == 'KEYWORD': #'void'|type
            self.process(newroot,'keyword')
        else:
            self.process(newroot,'identifier')
        self.process(newroot,'identifier') #subroutineName
        self.process(newroot,'symbol') #'(' 
        self.compileParameterList(newroot) #parameterList
        self.process(newroot,'symbol') #')'
        self.compileSubroutineBody(newroot)  #subroutineBody      

    def compileParameterList(self,root):
        #parameterList: ((type varName)(','type varName)*)?
        newroot = ET.SubElement(root, 'parameterList')
        newroot.text = '\n'
        newroot.tail = '\n'
        if self.tokenizer.current_token != ')': #parameterList?
            if self.tokenizer.tokenType() == 'KEYWORD': #type
                self.process(newroot,'keyword')
            else:
                self.process(newroot,'identifier')
            self.process(newroot,'identifier') #varName
            while self.tokenizer.current_token != ')': #(','type varName)*
                self.process(newroot,'symbol')  #','
                if self.tokenizer.tokenType() == 'KEYWORD': #type
                    self.process(newroot,'keyword')
                else:
                    self.process(newroot,'identifier')
                self.process(newroot,'identifier')  #varName

    def compileSubroutineBody(self,root):
        #subroutineBody:'{'varDec*statements'}'
        newroot = ET.SubElement(root, 'subroutineBody')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.process(newroot,'symbol')  #'{'
        while self.tokenizer.current_token == 'var': #varDec*
            self.compileVarDec(newroot)
        self.compileStatements(newroot) #statements
        self.process(newroot,'symbol')  #'}'    

    def compileVarDec(self,root):
        #varDec: 'var' type varName (',' varName)*';'
        newroot = ET.SubElement(root, 'varDec')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.process(newroot,'keyword') #'var'
        if self.tokenizer.tokenType() == 'KEYWORD': #type
            self.process(newroot,'keyword')
        else:
            self.process(newroot,'identifier')
        self.process(newroot,'identifier')  #varName
        while self.tokenizer.current_token != ';': #(','varName)*
            self.process(newroot,'symbol') 
            self.process(newroot,'identifier')
        self.process(newroot,'symbol') #';'        

    def compileStatements(self,root):
        #statements:statement*
        newroot = ET.SubElement(root, 'statements')
        newroot.text = '\n'
        newroot.tail = '\n'
        while self.tokenizer.current_token in ['let','if','while','do','return']:#statement*
            if self.tokenizer.current_token == 'let':
                self.compileLet(newroot)
            elif self.tokenizer.current_token == 'if':
                self.compileIf(newroot)
            elif self.tokenizer.current_token == 'while':
                self.compileWhile(newroot)
            elif self.tokenizer.current_token == 'do':
                self.compileDo(newroot)
            elif self.tokenizer.current_token == 'return':
                self.compileReturn(newroot)

    def compileLet(self,root):
        #letStatement: 'let' varName ('['expression']')? '=' expression ';'
        newroot = ET.SubElement(root, 'letStatement')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.process(newroot,'keyword') #'let'
        self.process(newroot,'identifier')  #varName
        if self.tokenizer.current_token == '[': #('['expression']')?
            self.process(newroot,'symbol')
            self.compileExpression(newroot)
            self.process(newroot,'symbol')
        self.process(newroot,'symbol') #'='
        self.compileExpression(newroot) #expression
        self.process(newroot,'symbol') #';'

    def compileIf(self,root):
        #ifStatement: 'if' '('expression')' '{'statements'}' ('else' '{'statements'}')?
        newroot = ET.SubElement(root, 'ifStatement')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.process(newroot,'keyword') #'if'
        self.process(newroot,'symbol') #'('
        self.compileExpression(newroot) #expression
        self.process(newroot,'symbol') #')'
        self.process(newroot,'symbol') #'{'
        self.compileStatements(newroot) #statements
        self.process(newroot,'symbol') #'}'
        if self.tokenizer.current_token == 'else': #('else' '{'statements'}')?
            self.process(newroot,'keyword') #'else'
            self.process(newroot,'symbol') #'{'
            self.compileStatements(newroot) #statements
            self.process(newroot,'symbol') #'}'

    def compileWhile(self,root):
        """
        print("<whileStatement>")
        process("while")
        process("(")
        compileExpression()
        process(")")
        process("{")
        compileStatements()
        process("}")
        print("</whileStatement>")
        """
        #whileStatement:'while''('expression')''{'statements'}'
        newroot = ET.SubElement(root, 'whileStatement')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.process(newroot,'keyword') #'while'
        self.process(newroot,'symbol') #'('
        self.compileExpression(newroot) #expression
        self.process(newroot,'symbol') #')'
        self.process(newroot,'symbol') #'{'
        self.compileStatements(newroot) #statements
        self.process(newroot,'symbol') #'}'

    def compileDo(self,root):
        #doStatement: 'do' subroutineCall ';'
        #subroutineCall: subroutineName '(' expressionlist ')' | (className|varName)'.'subroutineName '(' expressionlist ')'
        newroot = ET.SubElement(root, 'doStatement')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.process(newroot,'keyword') #'do'
        self.process(newroot,'identifier') # subroutineName | (className|varName)
        if self.tokenizer.current_token == '.': #(className|varName)'.'subroutineName '(' expressionlist ')'
            self.process(newroot,'symbol') #'.'
            self.process(newroot,'identifier') #subroutineName
            self.process(newroot,'symbol') #'('
            self.compileExpressionList(newroot) #expressionlist
            self.process(newroot,'symbol') #')'
        elif self.tokenizer.current_token == '(':
            self.process(newroot,'symbol') #'('
            self.compileExpressionList(newroot) #expressionlist
            self.process(newroot,'symbol') #')'
        self.process(newroot,'symbol') #';'

    def compileReturn(self,root):
        #returnStatement: 'return' expression? ';'
        newroot = ET.SubElement(root, 'returnStatement')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.process(newroot,'keyword') #'return'
        if self.tokenizer.current_token != ';':
            self.compileExpression(newroot)
        self.process(newroot,'symbol') #';'     

    def compileExpression(self,root):
        #expression: term (op term)*
        newroot = ET.SubElement(root, 'expression')
        newroot.text = '\n'
        newroot.tail = '\n'
        self.compileTerm(newroot) #term
        while self.tokenizer.current_token not in [';',')',',',']','}']: #()*
            self.process(newroot,'symbol') #op
            self.compileTerm(newroot) #term

    def compileTerm(self,root):
        #term: integerConstant|stringConstant|keywordConstant|varName|
        # varName '['expression']'|subroutineCall|'('expression')'|unaryOp term
        newroot = ET.SubElement(root, 'term')
        newroot.text = '\n'
        newroot.tail = '\n'
        if self.tokenizer.tokenType() == 'KEYWORD':
            self.process(newroot,'keyword') #keywordConstant
        elif self.tokenizer.tokenType() == 'INT_CONST':
            self.process(newroot,'integerConstant') #integerConstant
        elif self.tokenizer.tokenType() == 'STRING_CONST':
            self.process(newroot,'stringConstant') #stringConstant
        elif self.tokenizer.tokenType() == 'IDENTIFIER':
            #varName| varName '['expression']'|subroutineCall
            if self.tokenizer.tokens[0] == '[': #varName '['expression']'
                self.process(newroot,'identifier') #varName
                self.process(newroot,'symbol') #'['
                self.compileExpression(newroot)
                self.process(newroot,'symbol') #']'
            elif self.tokenizer.tokens[0] in ['.','(']: #subroutineCall
                self.process(newroot,'identifier') # subroutineName | (className|varName)
                if self.tokenizer.current_token == '.': #(className|varName)'.'subroutineName '(' expressionlist ')'
                    self.process(newroot,'symbol') #'.'
                    self.process(newroot,'identifier') #subroutineName
                    self.process(newroot,'symbol') #'('
                    self.compileExpressionList(newroot) #expressionlist
                    self.process(newroot,'symbol') #')'
                elif self.tokenizer.current_token == '(':
                    self.process(newroot,'symbol') #'('
                    self.compileExpressionList(newroot) #expressionlist
                    self.process(newroot,'symbol') #')'
            else: 
                self.process(newroot,'identifier') #varName          
        elif self.tokenizer.current_token == '(': # '('expression')'
            self.process(newroot,'symbol') #'('
            self.compileExpression(newroot)
            self.process(newroot,'symbol') #')'
        elif self.tokenizer.current_token in ['~','-']:# unaryOp term
            self.process(newroot,'symbol') # unaryOp: '~'|'-'
            self.compileTerm(newroot)
            
    def compileExpressionList(self,root):
        #expressionList: (expression (','expression)*)?
        newroot = ET.SubElement(root, 'expressionList')
        newroot.text = '\n'
        newroot.tail = '\n'
        if self.tokenizer.current_token != ')':  #()?
            self.compileExpression(newroot) #expression
            while self.tokenizer.current_token != ')':
                self.process(newroot,'symbol') #','
                self.compileExpression(newroot) #expression





