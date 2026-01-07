// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here:
(START)
	@R15
	D=M
	@length
	M=D //init length to be the arr length
	@R14
	D=M
	@arr
	M=D //init arr to be the start of the arr
	
	@arr
    A=M //put the address in arr in A
    D=M //put in D the value in arr[0]
    @min //set min to be arr[0]
    M=D
    @max //set max to be arr[0]
    M=D
	
    @minIndex
    M=0 
    @maxIndex
    M=0
	
    @i
    M=1
	@j
	M=1
	
(FINDMIN)
	@length
	D=M
	@i
	D=D-M
	@FINDMAX
	D;JEQ //if (length-i)=0 then jump to find-max
	
	@i
	D=M //D contains the value of i
	@arr
	A=M
	D=D+A // d=arr+i
	A=D //set A to current address
	D=M //put in D the value of arr[i]
	
	@min
	D=D-M // check if arr[i]-min < 0 if so then arr[i] is smaller than min
	@CHANEGMIN
	D;JLT
	
	@i
	M=M+1
	@FINDMIN
	0;JMP
	
(CHANEGMIN)
	@i
    D=M //put in D the current element index
    @minIndex
    M=D //change minIndex to current index
	
	@i
    D=M
    @arr
    A=M
    D=D+A  // D = arr + i
    A=D
    D=M
    @min
    M=D //put in min the new value
	
	@i
    M=M+1 //increase i
    @FINDMIN
    0;JMP

(FINDMAX)
	@length
	D=M
	@j
	D=D-M //if (length-j)=0 jump to CONT
	@CONT
	D;JEQ
	
	@j
	D=M
	@arr
	A=M
	D=D+A  // D contains arr+j index
    A=D
    D=M   // D=arr[j]
	
	@max
	D=D-M //check if arr[i]- max > 0 if so then arr[j] is bigger than max
	@CHANEGMAX
	D;JGT
	
	@j
	M=M+1 //increase j
	@FINDMAX
	0;JMP
	
(CHANEGMAX)
	@j
    D=M
    @maxIndex
    M=D
	
	@j
    D=M
    @arr
    A=M
    D=D+A   // D contains arr + j index
    A=D
    D=M
    @max
    M=D //update max to new value
	
	@j
    M=M+1 //increase j
    @FINDMAX
    0;JMP
	

(CONT)
	@minIndex
    D=M
    @maxIndex
    D=D-M
    @END
    D;JEQ //check if max and min are the same elemnt, if so no need to swap

	@min
	D=M
	@temp
	M=D //put min val in temp

	@minIndex
	D=M
	@arr
	A=M
	D=D+A      // D=arr+minIndex
	@R2
	M=D //put the computed index in R2
	
	@max
	D=M 
	@R2
	A=M
	M=D //set arr[minIndex] to be max val

	@maxIndex
	D=M
	@arr
	A=M
	D=D+A  // D = arr + maxIndex
	@R2
	M=D //put the computed index in R2
	
	@temp
	D=M
	@R2
	A=M
	M=D // put in arr[maxIndex] min val which was in temp
(END)
	@END
    0;JMP