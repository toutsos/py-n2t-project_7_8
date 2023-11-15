#VMParser.py
#Loren Peitso (template)
#
# (student completing)
#
# CS2011   Project 7/8 Stack Operations
#
# last updated 03 October 2022
#


class VMParser(object):

    CMD = 0
    ARG1 = 1
    ARG2 = 2
    
############################################
# Constructor

    def __init__(self, filePath):
        self.toParse = self.__filterFile( self.__loadFile(str(filePath)) )



############################################
# instance methods

    def advance(self):
        '''readsdput,
           returns false if there are no more commands.  '''
        if self.toParse:
            return self.toParse.pop(0)
        else:
            return False



############################################
# related functions

    #we can see the task of parsing is pretty stable overall
    #we only need to introduce the specific chunk identification
    #needed for Virtual Machine translation
    #
    #the new functions don't even conflict with what we had from chapter 6
    #I just left them out for added clarity
    #
    #note that these are functions, not methods, they do not have self
    #as argument zero because they do not need to refer to the Parser's data, self.toParse.
    #This is a way organize, keeping the slicing/dicing in the parser component but not
    #require other components to hold a parser instance to access these three functions


    def command(line):
        ''' Peturns the line's command.
            -line is a string representing a command in VM Language 
            When calling this function form another file, use VMParser.command( line )
        '''
        line_commands = line.split()
        return line_commands[0]

   
    def arg1(line):
        ''' Peturns the line's first argument.
            -line is a string representing a command in VM Language 
            When calling this function form another file, use VMParser.arg1( line )
        '''
        line_commands = line.split()
        return line_commands[1]


    def arg2(line):
        ''' Peturns the line's second argument.
            -line is a string representing a command in VM Language 
            When calling this function form another file, use VMParser.arg2( line )
        '''
        line_commands = line.split()
        return line_commands[2]




############################################
# private/utility methods

    def __toTestDotTxt(self):
        '''this is just for outputting our stripped file as a test
           this function will not be active in the final program'''

        file = open("test.txt","w")
        file.write("\n".join(self.toParse))
        file.close() 


    def __loadFile(self, fileName):
        '''Loads the file into memory.

           -fileName is a String representation of a file name,
           returns contents as a simple List'''
        
        fileList = []
        file = open(fileName,"r")
        
        for line in file:
            fileList.append(line)
            
        file.close()
        
        return fileList


    def __filterFile(self, fileList):
        '''Comments, blank lines and unnecessary leading/trailing whitespace are removed from the list.

           -fileList is a List representation of a file, one line per element
           returns the fully filtered List'''
        
        filteredList = []
        
        for line in fileList:
            line = self.__filterOutEOLComments(line)
            line = line.strip()               #leading and trailing whitespace removal
            
            if line:                          #empty line removal
                filteredList.append(line)
        
        return filteredList


    def __filterOutEOLComments(self, line):
        '''Removes end-of-line comments.

           -line is a string representing single line
           returns the filtered line, which may be empty'''

        index = line.find('//')
        if index >= 0:
            line = line[0:index]

        return line




