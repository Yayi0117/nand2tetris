// translate: push constant 7
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// translate: push constant 8
@8
D=A
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
