// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(OUTER)
    @16384
    D=A
    @addr
    M=D //set addr as current address
    @8192
    D=A
    @n
    M=D // set n as the total words needed to be manipulated
    @i
    M=0 // set i as 0
    @KBD
    D=M  //retrive value from KBD
    @WHITE
    D;JEQ  //if KBD=0 goto WHITE
    @BLACK
    D;JNE // if KBD≠0 goto BLACK

(WHITE)
    @i
    D=M
    @n
    D=D-M 
    @OUTER
    D;JEQ  // if i=n goto OUTER loop
    @addr
    A=M
    M=0  // set the selected regester as WHITE
    @addr
    M=M+1  // make the current address step forward
    @i
    M=M+1
    @WHITE
    0;JMP //Goto WHITE loop

(BLACK)
    @i
    D=M
    @n
    D=D-M 
    @OUTER
    D;JEQ // if i=n goto OUTER loop
    @addr
    A=M
    M=-1  // set the selected regester as BLACK
    @addr
    M=M+1  // make the current address step forward
    @i
    M=M+1
    @BLACK
    0;JMP   //Goto BLACK loop


