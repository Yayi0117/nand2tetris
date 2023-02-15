from JackTokenizer import *
from SymbolTable import *
from VMWriter import *

class CompilationEngine:
    terminals = {'keyword':'KEYWORD','symbol':'SYMBOL','identifier':'IDENTIFIER','integerConstant':'INT_CONST','stringConstant':'STRING_CONST'}

    def __init__(self,input,output):
        self.tokenizer = input
        self.output = output

    def process(self,terminaltype):
        current_type = self.tokenizer.tokenType()
        if current_type != self.terminals[terminaltype]:
            print(f'{self.tokenizer.current_token} is not a/an {terminaltype}')
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()     


    def compileClass(self):
        #class: 'class'className '{'classVarDec* subroutineDec*'}'
        self.tokenizer.advance()  #first advance
        self.global_tabel = SymbolTable()
        self.subroutine_table = SymbolTable()
        self.writer = VMWriter(self.output)
        self.labelcount = 0
        self.process('keyword') #'class'
        self.class_name = self.tokenizer.current_token
        self.process('identifier') #classname
        self.process('symbol') #'{'
        while self.tokenizer.current_token in ['field', 'static']:  #classVarDec*
            self.compileClassVarDec()
        while self.tokenizer.current_token in ['constructor','function','method']:  #subroutineDec*
            self.compileSubroutine()
        self.process('symbol')#'}'

    def compileClassVarDec(self):
        # classVarDec: ('field'|'static') type varName (','varName)*';'
        var_kind = self.tokenizer.current_token
        self.process('keyword') #'field'|'static'
        var_type = self.tokenizer.current_token
        if self.tokenizer.tokenType() == 'KEYWORD': #type
            self.process('keyword')
        else:
            self.process('identifier')
        var_name = self.tokenizer.current_token
        self.global_tabel.define(var_name,var_type,var_kind)
        self.process('identifier') #varName
        while self.tokenizer.current_token != ';': #(','varName)*
            self.process('symbol') 
            var_name = self.tokenizer.current_token
            self.global_tabel.define(var_name,var_type,var_kind)
            self.process('identifier')
        self.process('symbol') #';'         

    def compileSubroutine(self):
        #subroutineDec: ('constructor'|'function'|'method')('void'|type)subroutineName'('parameterList')'
        # '{'varDec* subroutineBody
        self.subroutine_table.reset()   #Each time a subroutine starts running,during runtime, it gets a fresh set of local variables; each time a subroutine returns, its local variables are recycled
        keyword = self.tokenizer.current_token
        self.process('keyword')#'constructor'|'function'|'method'
        if self.tokenizer.tokenType() == 'KEYWORD': #'void'|type
            self.process('keyword')
        else:
            self.process('identifier')
        subroutine_name = self.class_name+'.'+self.tokenizer.current_token
        self.process('identifier') #subroutineName
        self.process('symbol') #'(' 
        self.compileParameterList(keyword) #parameterList
        self.process('symbol') #')'
        self.process('symbol')  #'{'
        while self.tokenizer.current_token == 'var': #varDec*
            self.compileVarDec()    
        nVars = self.subroutine_table.varCount('local') 
        self.writer.writeFunction(subroutine_name,nVars)        
        if keyword == 'method':            
            self.writer.writePush('argument',0)
            self.writer.writePop('pointer',0)
        if keyword == 'constructor':
            field_num = self.global_tabel.varCount('field')
            self.writer.writePush('constant',field_num)
            self.writer.writeCall('Memory.alloc',1)
            self.writer.writePop('pointer',0)
        self.compileSubroutineBody()  #subroutineBody      

    def compileParameterList(self,keyword):
        #parameterList: ((type varName)(','type varName)*)?
        if keyword == 'method':
            self.subroutine_table.define('this',self.class_name,'argument') #add this to the argument segment
        if self.tokenizer.current_token != ')': #parameterList?
            para_type = self.tokenizer.current_token
            if self.tokenizer.tokenType() == 'KEYWORD': #type
                self.process('keyword')
            else:
                self.process('identifier')
            para_name = self.tokenizer.current_token
            self.subroutine_table.define(para_name,para_type,'argument')
            self.process('identifier') #varName
            while self.tokenizer.current_token != ')': #(','type varName)*
                self.process('symbol')  #','
                para_type = self.tokenizer.current_token
                if self.tokenizer.tokenType() == 'KEYWORD': #type
                    self.process('keyword')
                else:
                    self.process('identifier')
                para_name = self.tokenizer.current_token
                self.subroutine_table.define(para_name,para_type,'argument')
                self.process('identifier')  #varName

    def compileSubroutineBody(self):
        #subroutineBody: statements'}'
        self.compileStatements() #statements
        self.process('symbol')  #'}'    

    def compileVarDec(self):
        #varDec: 'var' type varName (',' varName)*';'
        self.process('keyword') #'var'
        local_type = self.tokenizer.current_token 
        if self.tokenizer.tokenType() == 'KEYWORD': #type
            self.process('keyword')
        else:
            self.process('identifier')
        local_name = self.tokenizer.current_token
        self.subroutine_table.define(local_name,local_type,'local')
        self.process('identifier')  #varName
        while self.tokenizer.current_token != ';': #(','varName)*
            self.process('symbol') 
            local_name = self.tokenizer.current_token
            self.subroutine_table.define(local_name,local_type,'local')
            self.process('identifier')
        self.process('symbol') #';'        

    def compileStatements(self):
        #statements:statement*
        while self.tokenizer.current_token in ['let','if','while','do','return']:#statement*
            if self.tokenizer.current_token == 'let':
                self.compileLet()
            elif self.tokenizer.current_token == 'if':
                self.compileIf()
            elif self.tokenizer.current_token == 'while':
                self.compileWhile()
            elif self.tokenizer.current_token == 'do':
                self.compileDo()
            elif self.tokenizer.current_token == 'return':
                self.compileReturn()

    def compileLet(self):
        #letStatement: 'let' varName ('['expression']')? '=' expression ';'
        self.process('keyword') #'let'
        varName = self.tokenizer.current_token
        if varName in self.subroutine_table.table:
            kind = self.subroutine_table.kindOf(varName)
            index = self.subroutine_table.indexOf(varName)
        else:
            kind = self.global_tabel.kindOf(varName)
            if kind == 'field':
                kind = 'this'
            index = self.global_tabel.indexOf(varName)
        self.process('identifier')  #varName
        if self.tokenizer.current_token == '[': #('['expression']')?
            '''
            let arr[expression1] = expression2:
            push arr
            //// call compileExpression to compute and push expression1
            add // top stack value = address of arr[expression1]
            //// call compileExpression to compute and push expression2
            pop temp 0 // temp 0 = the value of expression2
            pop pointer 1
            push temp 0
            pop that 0
            '''
            self.process('symbol') #'['
            self.writer.writePush(kind,index)
            self.compileExpression()
            self.writer.writeArithmetic('+')
            self.process('symbol')#']'
            self.process('symbol') #'='
            self.compileExpression() #expression
            self.process('symbol') #';'
            self.writer.writePop('temp',0)
            self.writer.writePop('pointer',1)
            self.writer.writePush('temp',0)
            self.writer.writePop('that',0)
        else:        
            self.process('symbol') #'='
            self.compileExpression() #expression
            self.process('symbol') #';'
            self.writer.writePop(kind,index)

    def compileIf(self):
        #ifStatement: 'if' '('expression')' '{'statements'}' ('else' '{'statements'}')?
        self.process('keyword') #'if'
        self.process('symbol') #'('
        self.compileExpression() #expression
        self.writer.writeArithmetic('~')
        self.process('symbol') #')'
        self.process('symbol') #'{'
        label_1 = f'IF_{self.labelcount}'
        self.labelcount += 1
        self.writer.writeIf(label_1)
        self.compileStatements() #statements
        self.process('symbol') #'}'
        if self.tokenizer.current_token == 'else': #('else' '{'statements'}')?
            label_2 = f'IF_{self.labelcount}'
            self.labelcount += 1
            self.writer.writeGoto(label_2)
            self.writer.writeLabel(label_1)
            self.process('keyword') #'else'
            self.process('symbol') #'{'
            self.compileStatements() #statements
            self.process('symbol') #'}'
            self.writer.writeLabel(label_2)
        else:
            self.writer.writeLabel(label_1)


    def compileWhile(self):
        #whileStatement:'while''('expression')''{'statements'}'
        label_1 = f'WHILE_{self.labelcount}'
        self.labelcount += 1
        self.writer.writeLabel(label_1)
        self.process('keyword') #'while'
        self.process('symbol') #'('
        self.compileExpression() #expression
        self.writer.writeArithmetic('~')
        label_2 = f'IF_{self.labelcount}'
        self.labelcount += 1
        self.writer.writeIf(label_2)
        self.process('symbol') #')'
        self.process('symbol') #'{'
        self.compileStatements() #statements
        self.process('symbol') #'}'
        self.writer.writeGoto(label_1)
        self.writer.writeLabel(label_2)
        

    def compileDo(self):
        #doStatement: 'do' subroutineCall ';'
        #subroutineCall: subroutineName '(' expressionlist ')' | (className|varName)'.'subroutineName '(' expressionlist ')'
        self.process('keyword') #'do'
        self.compileExpression()
        self.process('symbol') #';'
        self.writer.writePop('temp',0)

    def compileReturn(self):
        #returnStatement: 'return' expression? ';'
        self.process('keyword') #'return'
        if self.tokenizer.current_token != ';':
            self.compileExpression()
            self.writer.writeReturn()
        else:
            self.writer.writePush('constant',0)
            self.writer.writeReturn()        
        self.process('symbol') #';'   

    def compileExpression(self):
        #expression: term (op term)*
        self.compileTerm() #term
        while self.tokenizer.current_token not in [';',')',',',']','}']: #()*
            operator = self.tokenizer.current_token
            self.process('symbol') #op
            self.compileTerm() #term
            if operator in ['&','|','~','=','>','<','+','-']:
                self.writer.writeArithmetic(operator)
            elif operator == '*':
                self.writer.writeCall('Math.multiply',2)
            elif operator == '/':
                self.writer.writeCall('Math.divide',2)
            else:
                print(f'{operator} is an illegal operator')

    def compileTerm(self):
        #term: integerConstant|stringConstant|keywordConstant|varName|
        # varName '['expression']'|subroutineCall|'('expression')'|unaryOp term
        if self.tokenizer.tokenType() == 'KEYWORD':
            if self.tokenizer.current_token == 'true':
                self.writer.writePush('constant',1)
                self.writer.writeArithmetic('-',1)
            if self.tokenizer.current_token in ['false','null']:
                self.writer.writePush('constant',0)
            if self.tokenizer.current_token == 'this':
                self.writer.writePush('pointer',0)
            self.process('keyword') #keywordConstant
        elif self.tokenizer.tokenType() == 'INT_CONST':
            self.writer.writePush('constant',self.tokenizer.intVal())
            self.process('integerConstant') #integerConstant
        elif self.tokenizer.tokenType() == 'STRING_CONST':
            string_const = self.tokenizer.stringVal()
            self.writer.writePush('constant',len(string_const))
            self.writer.writeCall('String.new',1)
            for char in string_const:
                self.writer.writePush('constant', ord(char))   
                self.writer.writeCall('String.appendChar', 2)        
            self.process('stringConstant') #stringConstant
        elif self.tokenizer.tokenType() == 'IDENTIFIER':
            #varName| varName '['expression']'|subroutineCall
            varName = self.tokenizer.current_token
            if varName in self.subroutine_table.table:
                scope = 0
                obj_type = self.subroutine_table.typeof(varName)
                kind = self.subroutine_table.kindOf(varName)
                index = self.subroutine_table.indexOf(varName)
            elif varName in self.global_tabel.table:
                scope = 1
                obj_type = self.global_tabel.typeof(varName)
                kind = self.global_tabel.kindOf(varName)
                if kind == 'field':
                    kind = 'this'
                index = self.global_tabel.indexOf(varName)
            else:
                scope = 2 # a classname or subroutinename
            if self.tokenizer.tokens[0] == '[': #varName '['expression']'
                '''
                arr[expression]:
                push arr
                push expression1
                add
                pop pointer 1
                posh that 0
                '''
                self.writer.writePush(kind,index)
                self.process('identifier') #varName
                self.process('symbol') #'['
                self.compileExpression()
                self.writer.writeArithmetic('+')
                self.writer.writePop('pointer',1)
                self.writer.writePush('that',0)
                self.process('symbol') #']'
            elif self.tokenizer.tokens[0] in ['.','(']: #subroutineCall
                self.process('identifier') # subroutineName | (className|varName)
                if self.tokenizer.current_token == '.': #(className|varName)'.'subroutineName '(' expressionlist ')'
                    self.process('symbol') #'.'
                    if scope == 0 or scope == 1:  # a method call
                        subName = obj_type + '.' + self.tokenizer.current_token
                        self.process('identifier') #subroutineName
                        self.process('symbol') #'('
                        self.writer.writePush(kind,index)
                        nArgs = self.compileExpressionList()+1 #expressionlist
                        self.process('symbol') #')'
                        self.writer.writeCall(subName,nArgs)
                    elif scope == 2: # a construction call
                        subName = varName + '.' +self.tokenizer.current_token
                        self.process('identifier') #subroutineName
                        self.process('symbol') #'('
                        nArgs = self.compileExpressionList() #expressionlist
                        self.process('symbol') #')'
                        self.writer.writeCall(subName,nArgs)             
                elif self.tokenizer.current_token == '(': # a function call from current class
                    subName = self.class_name+'.'+varName
                    self.process('symbol') #'('
                    self.writer.writePush('pointer',0) 
                    nArgs = self.compileExpressionList()+1 #expressionlist
                    self.process('symbol') #')'
                    self.writer.writeCall(subName,nArgs)
            else: # only a varName
                self.process('identifier') #varName
                self.writer.writePush(kind,index)
        elif self.tokenizer.current_token == '(': # '('expression')'
            self.process('symbol') #'('
            self.compileExpression()
            self.process('symbol') #')'
        elif self.tokenizer.current_token in ['~','-']:# unaryOp term
            operator = self.tokenizer.current_token
            self.process('symbol') # unaryOp: '~'|'-'
            self.compileTerm()
            self.writer.writeArithmetic(operator,1)
            
    def compileExpressionList(self):
        #expressionList: (expression (','expression)*)?
        nArgs = 0
        if self.tokenizer.current_token != ')':  #()?
            self.compileExpression() #expression
            nArgs += 1
            while self.tokenizer.current_token != ')':
                self.process('symbol') #','
                self.compileExpression() #expression
                nArgs += 1
        return nArgs





