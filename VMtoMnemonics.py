#!/usr/bin/python

#VMtoMnemonics.py
#Loren Peitso (template)
#
# (student completing)
#
# CS2011   Project 7/8 Stack Operations
#
# last updated 03 October 2022
#
import sys  #for command line launch functionality

from pathlib import * 

from VMParser import *
from VMCodeGenerator import *

# constants to manage differences between chapter 7 & 8 examples
#   you will not need to uses/manipulate these, where they are used in 
#   code that will toucy yours, I have already laid the reference in via the scaffolding
FILE = 0
COMPLEX_INIT = 1

    
class VMtoMnemonics(object):


##########################################
#Constructor

    def __init__(self, target):
        
        self.targetPath = Path(target[FILE])
        self.GEN_INIT = target[COMPLEX_INIT]

        if self.targetPath.is_dir():
            self.outputFilePath = self.targetPath / (self.targetPath.name + '.asm')

        else:
            if self.targetPath.suffix == '.vm':
                self.outputFilePath = Path(self.targetPath.parent / (self.targetPath.stem + '.asm'))

            else:
                raise RuntimeError( "error, cannot use the filename: " + target[FILE] )



##########################################
#public methods

    def process(self):
        ''' Processes the entire target being compiled.
            The target may be a directory with multuple /.vm files or it
            may be a single file. Returns a List comprised of the results
            from translating each individual file. 
        '''
        
        assemblyCode = []

        #managing for per-test-case requirements
        codeGenerator = VMCodeGenerator( self.targetPath )
        if self.GEN_INIT:
            assemblyCode.extend( codeGenerator.generateInit() )

        if self.targetPath.is_dir(): #   if self.targetPath is a directory
            #   in the directory, no .asm output is necessary, nor needed to be correct
            for file_path in Path(self.targetPath).glob('*.vm'):
                assemblyCode.extend(self.__processFile(file_path))
        else:  #if self.targetPath is a single file
            assemblyCode.extend(self.__processFile(self.targetPath))

        assemblyCode.extend(codeGenerator.secureEndOfCode())
        return self.__output(assemblyCode)


##########################################
#private methods
        
    def __processFile(self, filePath):
        ''' Processes a single file, returning the translated assembler code. 
            -filepath is a Pathlib Path object referring to a single file to be translated.
        '''

        # You can call a new instance of codeGenerator here

        parser = VMParser(filePath)
        codeGenerator = VMCodeGenerator(filePath)
        assemblyCode = []

        line = parser.advance()
        while line:
            assemblyCode.extend(codeGenerator.translateLine(line))
            line = parser.advance()
        return assemblyCode



    def __output(self, codeList):
        ''' Writes the List codelist into a file, returning the filename of the result.
            -codeList a List of assembly commands 
        '''
        file = open(str(self.outputFilePath),"w")
        file.write("\n".join(codeList))
        file.close()
        return str(self.outputFilePath)


    
 
#################################
#################################
#################################
#this kicks off the program and assigns the argument to a variable
#
if __name__=="__main__":

    target = eval(sys.argv[1])     # use this one for final deliverable
    
      #chapter 7 test content    
    # target = ('StackArithmetic/SimpleAdd', False)      # for internal IDLE testing only
    # target = ('StackArithmetic/StackTest', False)      # for internal IDLE testing only
    # target = ('MemoryAccess/BasicTest', False)         # for internal IDLE testing only
    # target = ('MemoryAccess/PointerTest', False)       # for internal IDLE testing only
    # target = ('MemoryAccess/StaticTest', False)        # for internal IDLE testing only

      #chapter 8 test content 
    # target = ('ProgramFlow/BasicLoop', False)          # for internal IDLE testing only
    # target = ('ProgramFlow/FibonacciSeries', False)    # for internal IDLE testing only
    # target = ('FunctionCalls/SimpleFunction', False)   # for internal IDLE testing only
    # target = ('FunctionCalls/NestedCall', True)        # for internal IDLE testing only
    # target = ('FunctionCalls/FibonacciElement', True)  # for internal IDLE testing only
    # target = ('FunctionCalls/StaticsTest', True)       # for internal IDLE testing only

    translator = VMtoMnemonics(target)
    print('\n' + str( translator.process() ) + ' has  been translated.')


