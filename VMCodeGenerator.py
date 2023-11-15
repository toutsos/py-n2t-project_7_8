#VMCodeGenerator.py
#Loren Peitso (template)
#
# (student completing)
#
# CS2011   Project 7/8 Stack Operations
#
# last updated 03 October 2022
#
from pathlib import *

from VMParser import *

# Per architecture standard from book
POINTER_START = 3
TEMP_START = 5

class VMCodeGenerator(object):

    unary = {'neg':'-', 'not':'!'}
    binary = {'add':'+', 'sub':'-', 'and':'&', 'or':'|'}
    seg_abbrev = {'local': 'LCL', 'argument': 'ARG', 'this': 'THIS', 'that': 'THAT'}
    label_dict = {}

    
############################################
# Constructor    
    def __init__(self, filePath):

        #fileName is used for static partition name creation,
        #   stem just takes the part to the left of the dot
        self.fileName = filePath.stem

        self.currentFunction = None #
        self.labelID = 0
        # self.lineCount = 0 #This line counter is used in order to have a unique identifier for each line translated, so that we have a unique label for the theoritically same code generated

        #a little functional programming avoids well over 100 lines of code just
        # managing the two-stage lookups

        #chapter 7 content to implement
        self.tokenToCommandDict = {
    
                'add' : self.__arithmetic,
                'sub' : self.__arithmetic,
                'neg' : self.__arithmetic,
                'and' : self.__arithmetic,
                 'or' : self.__arithmetic,
                'not' : self.__arithmetic,
            
                 'eq' : self.__conditional,
                 'gt' : self.__conditional,
                 'lt' : self.__conditional,
    
               'push' : self.__push,
                'pop' : self.__pop
        }


        #chapter 8 content to implement
        self.tokenToCommandDict['label'] = self.__generateLabel
        self.tokenToCommandDict['if-goto'] = self.__generateIf
        self.tokenToCommandDict['goto'] = self.__generateGoto

        self.tokenToCommandDict['function'] = self.__generateFunction
        self.tokenToCommandDict['return'] = self.__generateReturn
        self.tokenToCommandDict['call'] = self.__generateCall
        



############################################
# instance methods

    def translateLine(self, line):
        ''' Translates one single line/command.  
            -line is a string that represents a command.
            Returns the reanslated result.
        '''
        command = VMParser.command(line)
        return self.tokenToCommandDict[command](line)    #functional style call eliminating MANY dozens of lines of code
         

    ##
    def generateInit(self): 
        ''' Generation of Hack assembler code for program initialization:
                SP = 256.
                pointers = -1 (true)    #we add this beyond book requirement as a boot security technique
                Call Sys.Init()
        
            this code is only invoked for the last 3 cases of project08.
            Other test cases are manually set-up by the test script.
        '''
        lines = []
        lines.append('//generateInit')
        lines.append('@256')
        lines.append('D=A')
        lines.append('@SP')
        lines.append('M=D')
        lines.append('A=A+1')
        lines.append('M=-1')
        lines.append('A=A+1')
        lines.append('M=-1')
        lines.append('A=A+1')
        lines.append('M=-1')
        lines.append('A=A+1')
        lines.append('M=-1')
        lines.extend(self.translateLine('call Sys.init 0'))
        return lines

    ## Prevent to access memory locations after those used in execution of code.
    def secureEndOfCode(self):
        lines = []
        lines.append('(END)')
        lines.append('@END')
        lines.append('0;JMP')
        return lines

############################################
# private/utility methods

    def __arithmetic(self, command):
        ''' Handle generation of Hack assembler code for the basic
            arithmetic commands.
            -command is a string representing an arithmetic command.
            Returns a List of assembly code strings.
        '''
        lines = []
        lines.append('//__arithmetic')

        if command in self.unary:
            symbol = self.unary[command]
            lines.append('@SP')
            lines.append('A=M-1')
            lines.append('M=' + symbol + 'M')
        else:
            symbol = self.binary[command]
            lines.extend(self.__popStacktoD())
            lines.append('A=A-1')
            lines.append('M=M' + symbol + 'D')
        
        return lines


    def __conditional(self, command):
        ''' Handle generation of Hack assembler code for the basic conditional commands,
            arithmetic commands.
            -command is a string representing the boolean comparison operator, Hack VM
             lang provides it in lowercase.
            Returns a List of assembly code strings.
        '''
        command_of_line = VMParser.command(command).upper()
        label = str(self.__makeUniqueLabel())
        lines = []
        lines.append('//__conditional')
        lines.extend(self.__popStacktoD())
        lines.append('A=A-1')
        lines.append('D=M-D')
        lines.append('@'+self.__resolveSymbol()+'IF_SUCCESS_L'+label)
        lines.append('D;J'+command_of_line)
        lines.append('D=0')
        lines.append('@'+self.__resolveSymbol()+'IF_FAILURE_L'+label)
        lines.append('D;JMP')
        lines.append('('+self.__resolveSymbol()+'IF_SUCCESS_L'+label+')')
        lines.append('D=-1')
        lines.append('('+self.__resolveSymbol()+'IF_FAILURE_L'+label+')')
        lines.append('@SP')
        lines.append('A=M-1')
        lines.append('M=D')

        return lines


    def __push(self, line):
        ''' Handle generation of Hack assembler code for for command 'push'. 
            -line is a string representing the the 'push' command and its aruments.
            Returns a List of assembly code strings.
        '''

        lines = []
        lines.append('//__push')
        arg1 = VMParser.arg1(line)
        arg2 = VMParser.arg2(line)
        if arg1 == 'constant':
            lines.append('@'+arg2)
            lines.append('D=A')
            lines.extend(self.__pushDtoStack())
        elif (arg1 == 'static' or arg1 == 'pointer' or arg1=='temp'):
            if(arg1 == 'static'):
                name = self.fileName+'.'+arg2
            elif(arg1 == 'pointer'):
                name = str(POINTER_START+int(arg2))
            elif(arg1 == 'temp'):
                name = str(TEMP_START+int(arg2))
            lines.append('@'+name)
            lines.append('D=M')
            lines.extend(self.__pushDtoStack())
        else:
            arg1 = self.seg_abbrev[arg1]
            lines.extend(self.__pushFromSegment(arg1,arg2))

        return lines


    def __pop(self, line):
        ''' Handle generation of Hack assembler code for for command 'pop'. 
            -line is a string representing the the 'pop' command and its aruments.
            Returns a List of assembly code strings.
        '''
        arg1 = VMParser.arg1(line)
        arg2 = VMParser.arg2(line)
        lines = []
        lines.append('//__pop')
        if( arg1 in self.seg_abbrev):
            arg1 = self.seg_abbrev[arg1]
            lines.extend(self.__popToSegment(arg1,arg2))
        elif (arg1 == 'static' or arg1 == 'pointer' or arg1 == 'temp'):
            if(arg1 == 'static'):
                name = self.fileName+'.'+arg2 # filename.arg2 is the new unique name for the static memory address
            elif(arg1 == 'pointer'):
                name = str(POINTER_START+int(arg2)) # pointer location at memory
            elif (arg1 == 'temp'):
                name = str(TEMP_START+int(arg2))  # temp location at memory
            lines.append('@SP')
            lines.append('AM=M-1')
            lines.append('D=M')
            lines.append('@'+name)
            lines.append('M=D')
        return lines
            

    def __pushDtoStack(self):
        ''' helper function per name '''
        lines = []

        lines.append('@SP')
        lines.append('A=M')
        lines.append('M=D')
        lines.append('@SP')
        lines.append('M=M+1')

        return lines


    def __popStacktoD(self):
        ''' helper function per name '''
        lines = []
        lines.append('@SP')
        lines.append('AM=M-1')
        lines.append('D=M')

        return lines


    def __popToSegment(self, targetSegment, index):
        ''' helper function, manage the identical operations for segments: ARG, LCL, THIS, THAT '''
        lines = []
        lines.append('@'+targetSegment)
        lines.append('D=M')
        lines.append('@'+index)
        lines.append('D=D+A')
        lines.append('@R13')
        lines.append('M=D')
        lines.extend(self.__popStacktoD())
        lines.append('@R13')
        lines.append('A=M')
        lines.append('M=D')

        return lines
        
                
    def __pushFromSegment(self, targetSegment, index):
        ''' helper function, manage the identical operations for segments: ARG, LCL, THIS, THAT '''
        lines = []

        lines.append('@' + targetSegment)
        lines.append('D=M')
        lines.append('@' + index)
        lines.append('A=D+A')
        lines.append('D=M')
        lines.extend(self.__pushDtoStack())

        return lines


    def __makeUniqueLabel(self):
        ''' Create control logic labels labels need to be unique across a whole file per Hack 
            standard specified in fig 8.6. 
            Returns a uniqueifier string.
                note: function __resolveLabel() manages making any labels unique across
                a whole multi-file program
        '''
        self.labelID = self.labelID+1
        return self.labelID


    #################################################################
    ###  Chapter 8 additions

    def __resolveSymbol(self):
        ''' Creates globally unique symbols as per fig 8.6
               this function must be called anywere you make/transform a symbol!
               not only when executing __generateLabel() 
        '''
        if(self.currentFunction != None):
            return self.currentFunction+'$'
        else:
            return self.fileName+'.'

    def __generateLabel(self, line):
        ''' Generates and returns Hack assembler label code for function navigation
            when we find a VM label command.  '''
        loop_name = VMParser.arg1(line)
        lines = []
        lines.append('//__generateLabel')
        lines.append('('+self.__resolveSymbol()+loop_name+')')
        return lines

    ## goto
    def __generateGoto(self, line):
        ''' Generates and returns Hack assembler goto code for structured function navigation.
            -line is a string representing the the 'goto' command and its arument.
        '''

        label_name = VMParser.arg1(line)
        lines = []

        lines.append('//__generateGoto')
        lines.append('@'+self.__resolveSymbol()+label_name)
        lines.append('0;JMP')
        return lines


    ## ifgoto
    def __generateIf(self, line):
        ''' Generates and returns Hack assembler if-goto code for structured function navigation.
            -line is a string representing the the 'if-goto' command and its arument.
        '''
        loop_name = VMParser.arg1(line)
        lines = []
        lines.append('//__generateIf')
        lines.append('@SP')
        lines.append('AM=M-1')
        lines.append('D=M')
        lines.append('@'+self.__resolveSymbol()+loop_name)
        lines.append('D;JNE')
        return lines

    def __generateCall(self, line):
        ''' Generates and returns Hack assembler call code for structured function navigation.
            -line is a string representing the the 'call' command and its aruments.
        '''
        lines = []
        fnName = VMParser.arg1(line)
        numArgs = VMParser.arg2(line)
        label = str(self.__makeUniqueLabel())

        lines.append('//__generateCall' + ', '  + fnName + ', ' + numArgs)
        lines.append('@'+self.__resolveSymbol()+label)
        lines.append('D=A')
        lines.append('@SP')
        lines.append('A=M')
        lines.append('M=D')
        lines.append('@SP')
        lines.append('M=M+1')
        lines.append('@LCL')
        lines.append('D=M')
        lines.append('@SP')
        lines.append('A=M')
        lines.append('M=D')
        lines.append('@SP')
        lines.append('M=M+1')
        lines.append('@ARG')
        lines.append('D=M')
        lines.append('@SP')
        lines.append('A=M')
        lines.append('M=D')
        lines.append('@SP')
        lines.append('M=M+1')
        lines.append('@THIS')
        lines.append('D=M')
        lines.append('@SP')
        lines.append('A=M')
        lines.append('M=D')
        lines.append('@SP')
        lines.append('M=M+1')
        lines.append('@THAT')
        lines.append('D=M')
        lines.append('@SP')
        lines.append('A=M')
        lines.append('M=D')
        lines.append('@SP')
        lines.append('M=M+1')
        lines.append('@SP')
        lines.append('D=M')
        lines.append('@'+numArgs)
        lines.append('D=D-A')
        lines.append('@5')
        lines.append('D=D-A')
        lines.append('@ARG')
        lines.append('M=D')
        lines.append('@SP')
        lines.append('D=M')
        lines.append('@LCL')
        lines.append('M=D')
        lines.append('@'+fnName)
        lines.append('0;JMP')
        lines.append('('+self.__resolveSymbol()+label+')')
        return lines


    def __generateFunction(self, line):
        ''' Generates and returns Hack assembler function loading code for structured function navigation.
            responds to    function f k     as the form of the call
            -line is a string representing the 'function' command and its aruments.
        '''
        lines = []
        fnName = VMParser.arg1(line)
        numLocals = VMParser.arg2(line)
        self.currentFunction = fnName
        lines.append('//__generateFunction' + ', ' + fnName + ', ' + numLocals)
        lines.append('('+fnName+')')
        lines.append('D=0')
        for i in range(int(numLocals)):
            lines.append('@SP')
            lines.append('A=M')
            lines.append('M=D')
            lines.append('@SP')
            lines.append('M=M+1')
        return lines

    def __generateReturn(self, unused):
        ''' Generates and returns Hack assembler function return code for structured function navigation
            -unused is exactly what it says, it is required only for dynamic function calling consistency
        '''
        lines = []
        lines.append('//__generateReturn')
        lines.append('@LCL')
        lines.append('D=M')
        lines.append('@R15')
        lines.append('M=D')
        lines.append('@5')
        lines.append('A=D-A')
        lines.append('D=M')
        lines.append('@R14')
        lines.append('M=D')
        lines.append('@SP')
        lines.append('AM=M-1')
        lines.append('D=M')
        lines.append('@ARG')
        lines.append('A=M')
        lines.append('M=D')
        lines.append('D=A+1')
        lines.append('@SP')
        lines.append('M=D')
        lines.append('@R15')
        lines.append('AM=M-1')
        lines.append('D=M')
        lines.append('@THAT')
        lines.append('M=D')
        lines.append('@R15')
        lines.append('AM=M-1')
        lines.append('D=M')
        lines.append('@THIS')
        lines.append('M=D')
        lines.append('@R15')
        lines.append('AM=M-1')
        lines.append('D=M')
        lines.append('@ARG')
        lines.append('M=D')
        lines.append('@R15')
        lines.append('AM=M-1')
        lines.append('D=M')
        lines.append('@LCL')
        lines.append('M=D')
        lines.append('@R14')
        lines.append('A=M')
        lines.append('0;JMP')
        return lines





