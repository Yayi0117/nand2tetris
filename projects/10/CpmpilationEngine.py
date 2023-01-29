import xml.etree.cElementTree as ET
class CompilationEngine:
    termanals = ['keyword','symbol','identifier','integerConstant','stringConstant']

    def __init__(self,input,output):
        self.token = input
        self.output = output

    @classmethod
    def process(self,str):
        """
        A helper method that handles 
        the current token, and advances
        to get the next token.

        if (currentToken == str)
            printXMLToken(str)
        else
            print("syntax error")
        currentToken = tokenizer.advance()
        """
        


    def compileClass(self):
        root = ET.Element('class')  # generate file root 'class'
        root.text = '\n'
        root.tail = '\n'
        


    def compileClassVarDec(self):

    def compileSubroutine(self):

    def compileParameterList(self):

    def compileSubroutineBody(self):
    
    def compileVarDec(self):

    def compileStatements(self):

    def compileLet(self):

    def compileIf(self):

    def compileWhile(self):
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

    def compileDo(self):

    def compileReturn(self):

    def compileExpression(self):

    def compileTerm(self):

    def compileExpressionList(self):