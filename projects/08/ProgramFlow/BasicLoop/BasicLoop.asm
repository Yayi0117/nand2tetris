// translate: push constant 0    
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
// translate: pop local 0         
@LCL
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
(BasicLoop.LOOP_START)
// translate: push argument 0    
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// translate: push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// translate: add
@SP
M=M-1
A=M-1
D=M
@SP
A=M
D=M+D
@SP
A=M-1
M=D
// translate: pop local 0	        
@LCL
D=M
@0	
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// translate: push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
// translate: push constant 1
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// translate: sub
@SP
M=M-1
A=M-1
D=M
@SP
A=M
D=D-M
@SP
A=M-1
M=D
// translate: pop argument 0      
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
M=M-1
A=M
D=M
@R13
A=M
M=D
// translate: push argument 0
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
M=M-1
A=M
D=M
@BasicLoop.LOOP_START
D;JNE
// translate: push local 0
@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1
