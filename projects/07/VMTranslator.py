from parse import *
from codewriter import *
import sys  
import os
from pathlib import Path

def generation(parse,writer):  #generate assembly code
    while parse.has_more_commands():        
        if parse.commandType(parse.current) == 'C_ARITHMETIC':
            writer.WriteArithmetic(parse.content[parse.current])
        elif parse.commandType(parse.current) == 'C_PUSH' or parse.commandType(parse.current) == 'C_POP':
            segment = parse.arg1(parse.current)
            i = parse.arg2(parse.current)
            writer.WritePushPop(parse.content[parse.current],segment,i)
        parse.advance()

path = sys.argv[1]  #access command line argument
writer = CodeWriter(path) #creat an asm output file with the same name as the file or folder in the same directory
if os.path.isfile(path): #check whether a file or a folder is passed in
    parse = Parse(path)
    generation(parse,writer)
else: 
    files = [f for f in Path(path).iterdir() if os.path.splitext(f)[1]=='.vm'] # if a folder is passed in, access all pathes of vm files in it
    #foldername = os.path.basename(path)  get the folder's name from the path
    for file in files:
        writer.SetFileName(file)  #inform the code writer that the translation of a new VM file is started
        parse = Parse(file)
        generation(parse,writer)














