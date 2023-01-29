// translate: push constant 111
@111
D=A
@SP
A=M
M=D
@SP
M=M+1
// translate: push constant 333
@333
D=A
@SP
A=M
M=D
@SP
M=M+1
// translate: push constant 888
@888
D=A
@SP
A=M
M=D
@SP
M=M+1
// translate: pop static 8
@SP
M=M-1
A=M
D=M
@StaticTest.8
M=D
// translate: pop static 3
@SP
M=M-1
A=M
D=M
@StaticTest.3
M=D
// translate: pop static 1
@SP
M=M-1
A=M
D=M
@StaticTest.1
M=D
// translate: push static 3
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1
// translate: push static 1
@StaticTest.1
D=M
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
// translate: push static 8
@StaticTest.8
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
