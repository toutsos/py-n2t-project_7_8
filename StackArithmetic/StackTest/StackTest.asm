//__push
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//__conditional
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.IF_SUCCESS_L1
D;JEQ
D=0
@StackTest.IF_FAILURE_L1
D;JMP
(StackTest.IF_SUCCESS_L1)
D=-1
(StackTest.IF_FAILURE_L1)
@SP
A=M-1
M=D
//__push
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
//__conditional
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.IF_SUCCESS_L2
D;JEQ
D=0
@StackTest.IF_FAILURE_L2
D;JMP
(StackTest.IF_SUCCESS_L2)
D=-1
(StackTest.IF_FAILURE_L2)
@SP
A=M-1
M=D
//__push
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
//__conditional
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.IF_SUCCESS_L3
D;JEQ
D=0
@StackTest.IF_FAILURE_L3
D;JMP
(StackTest.IF_SUCCESS_L3)
D=-1
(StackTest.IF_FAILURE_L3)
@SP
A=M-1
M=D
//__push
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//__conditional
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.IF_SUCCESS_L4
D;JLT
D=0
@StackTest.IF_FAILURE_L4
D;JMP
(StackTest.IF_SUCCESS_L4)
D=-1
(StackTest.IF_FAILURE_L4)
@SP
A=M-1
M=D
//__push
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
//__conditional
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.IF_SUCCESS_L5
D;JLT
D=0
@StackTest.IF_FAILURE_L5
D;JMP
(StackTest.IF_SUCCESS_L5)
D=-1
(StackTest.IF_FAILURE_L5)
@SP
A=M-1
M=D
//__push
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
//__conditional
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.IF_SUCCESS_L6
D;JLT
D=0
@StackTest.IF_FAILURE_L6
D;JMP
(StackTest.IF_SUCCESS_L6)
D=-1
(StackTest.IF_FAILURE_L6)
@SP
A=M-1
M=D
//__push
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//__conditional
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.IF_SUCCESS_L7
D;JGT
D=0
@StackTest.IF_FAILURE_L7
D;JMP
(StackTest.IF_SUCCESS_L7)
D=-1
(StackTest.IF_FAILURE_L7)
@SP
A=M-1
M=D
//__push
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
//__conditional
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.IF_SUCCESS_L8
D;JGT
D=0
@StackTest.IF_FAILURE_L8
D;JMP
(StackTest.IF_SUCCESS_L8)
D=-1
(StackTest.IF_FAILURE_L8)
@SP
A=M-1
M=D
//__push
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
//__conditional
@SP
AM=M-1
D=M
A=A-1
D=M-D
@StackTest.IF_SUCCESS_L9
D;JGT
D=0
@StackTest.IF_FAILURE_L9
D;JMP
(StackTest.IF_SUCCESS_L9)
D=-1
(StackTest.IF_FAILURE_L9)
@SP
A=M-1
M=D
//__push
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
//__push
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
//__arithmetic
@SP
AM=M-1
D=M
A=A-1
M=M+D
//__push
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
//__arithmetic
@SP
AM=M-1
D=M
A=A-1
M=M-D
//__arithmetic
@SP
A=M-1
M=-M
//__arithmetic
@SP
AM=M-1
D=M
A=A-1
M=M&D
//__push
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
//__arithmetic
@SP
AM=M-1
D=M
A=A-1
M=M|D
//__arithmetic
@SP
A=M-1
M=!M
(END)
@END
0;JMP