// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// Multiplies R0 and R1 and stores the result in R2.
//
// Assumptions:
// - R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.
// - You can assume that you will only receive arguments that satisfy:
//   R0 >= 0, R1 >= 0, and R0*R1 < 32768.
// - Your program does not need to test these conditions.
//
// Requirements:
// - Your program should not change the values stored in R0 and R1.
// - You can implement any multiplication algorithm you want.

// Put your code here.
(START)
	@sum
	M=0 //init sum to 0
	@R1
	D=M
	@FINISH //test if any of the the vars is 0
	D;JEQ
	@R0
	D=M
	@FINISH //test if any of the the vars is 0
	D;JEQ
	@counter
	M=0 //init counter to 0
(LOOP)
	@R1
	D=M
	@counter
	D=D-M
	@ADD
	D;JGT
(FINISH)
	@sum
	D=M
	@R2
	M=D //set R2 to be the result of the mult
	@END
	0;JMP
(ADD)
	@R0
	D=M
	@sum
	M=M+D //add R0 another time
	@counter
	M=M+1 //increase counter in 1
	@LOOP
	0;JMP //jump back to loop start
(END)
	@END
	0;JMP
	