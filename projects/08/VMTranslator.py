from parse import *
from codewriter import *
import sys  
import os
from pathlib import Path

def generation(parse,writer):  #generate assembly code
    while parse.has_more_commands():        
        if parse.commandType(parse.current) == 'C_ARITHMETIC':
            writer.writeArithmetic(parse.content[parse.current])
        elif parse.commandType(parse.current) == 'C_PUSH' or parse.commandType(parse.current) == 'C_POP':
            segment = parse.arg1(parse.current)
            i = parse.arg2(parse.current)
            writer.writePushPop(parse.content[parse.current],segment,i)
        elif parse.commandType(parse.current) == 'C_LABEL':
            label = parse.content[parse.current][1]
            writer.writeLabel(label)
        elif parse.commandType(parse.current) == 'C_GOTO':
            label = parse.content[parse.current][1]
            writer.writeGoto(label)
        elif parse.commandType(parse.current) == 'C_IF':
            label = parse.content[parse.current][1]
            writer.writeIf(label)
        elif parse.commandType(parse.current) == 'C_CALL':
            functionName = parse.content[parse.current][1]
            numArgs = parse.content[parse.current][2]
            writer.writeCall(functionName,numArgs)
        elif parse.commandType(parse.current) == 'C_FUNCTION':
            functionName = parse.content[parse.current][1]
            numLocals = parse.content[parse.current][2]
            writer.writeFunction(functionName,numLocals)
        elif parse.commandType(parse.current) == 'C_RETURN':
            writer.writeReturn()        
        parse.advance()

path = sys.argv[1]  #access command line argument
writer = CodeWriter(path) #creat an asm output file with the same name as the file or folder in the same directory
if os.path.isfile(path): #check whether a file or a folder is passed in
    parse = Parse(path)
    generation(parse,writer)
else: 
    files = [f for f in Path(path).iterdir() if os.path.splitext(f)[1]=='.vm'] # if a folder is passed in, access all pathes of vm files in it
    #foldername = os.path.basename(path)  get the folder's name from the path
    writer.writeInite() # write the bootstrap for multiple vm files translation
    for file in files:
        writer.SetFileName(file)  #inform the code writer that the translation of a new VM file is started
        parse = Parse(file)
        generation(parse,writer)














