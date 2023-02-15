from CpmpilationEngine import *
from JackTokenizer import *
import sys  
import os
from pathlib import Path

def analyzer(file): 
    """
    this function is used to analyze one imput file
    """
    tokenizer = JackTokenizer(file)
    output = os.path.splitext(file)[0]+'.vm'
    c= CompilationEngine(tokenizer,output)
    c.compileClass()

path = sys.argv[1]  #access command line argument
if os.path.isfile(path): #check whether a file or a folder is passed in
    analyzer(path)
else: 
    # if a folder is passed in, access all pathes of vm files in it
    files = [f for f in Path(path).iterdir() if os.path.splitext(f)[1]=='.jack'] 
    for file in files:
        analyzer(file)