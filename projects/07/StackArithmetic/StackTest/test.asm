// translate: push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// translate: push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// translate: eq
@SP
M=M-1
A=M-1
D=M
@SP
A=M
D=M-D
M=0
@POSSITIVE
D;JEQ
@SP
A=M-1
M=0
(POSSITIVE)
@SP
A=M-1
M=-1
