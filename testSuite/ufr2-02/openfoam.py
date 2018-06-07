import os

class openfoamconstants:
        comment = "// ************************************************************************* //"

class list:
    
    def __init__(self, name, endWithSemicolon=True):
        self.name = name
        self.entries = []
        self.endWithSemicolon = endWithSemicolon

    def set(self, entries):
        self.entries = entries

    def add(self, entry):
        self.entries.append(entry)

    def writeToFile(self, file, indent):
        s = (self.name).rjust(indent*4+len(self.name))
        file.write( s )
        file.write( "\n" )
        
        file.write( ("(\n").rjust(indent*4+2) )
        numKeys = len(self.entries)
        for i in range(numKeys):
            e0 = self.entries[i]
            if type(e0) != type(str()):
                e0.writeToFile( file, indent+1 )
            else:
                s = "    %s\n" % (e0 )
                file.write( (s).rjust( indent*4+len(s) ) )
        if self.endWithSemicolon:
                file.write( (");\n").rjust(indent*4+3) )
        else:
                file.write( (")\n").rjust(indent*4+3) )

    def write(self, indent):
        s = (self.name).rjust(indent*4+len(self.name))
        print( s )
        
        print( ("(").rjust(indent*4+1) )
        numKeys = len(self.entries)
        for i in range(numKeys):
            e0 = self.entries[i]
            if type(e0) != type(str()):
                e0.write( indent+1 )
            else:
                s = "    %s" % (e0 )
                print( (s).rjust( indent*4+len(s) ) )
        if self.endWithSemicolon:
                print( (");\n").rjust(indent*4+2) )
        else:
                print( (")\n").rjust(indent*4+2) )

class dictionary:
    
    def __init__(self, name):
        self.name = name
        self.entries = {}

    def add(self, entry):
        self.entries.update(entry)

    def write(self):
        print self.name
        print "{"
        numKeys = len(self.entries.items())
        for i in range(numKeys):
            print "    %-20s %s;" % ( self.entries.items()[i][0], self.entries.items()[i][1] )
        print "}"

    def writeToFile(self, file, indent, headless=False):

        if not headless:
            s = (self.name).rjust(indent*4+len(self.name))
            file.write( s )
            file.write( "\n" )

        file.write( ("{\n").rjust(indent*4+2) )
        numKeys = len(self.entries.items())
        for i in range(numKeys):
            e0 = self.entries.items()[i][0]
            e1 = self.entries.items()[i][1]
            if type(e1) != type(str()):
                e1.writeToFile( file, indent+1 )
            else:
                s = "    %-24s %s;\n" % (e0 , e1 )
                file.write( (s).rjust( indent*4+len(s) ) )
        file.write( ("}\n").rjust(indent*4+2) )


class header:

    def __init__(self, name, object, location, type):

        self.dict = dictionary( name )
        self.dict.add( { "object" : object } )
        self.dict.add( { "format" : "ascii" } )
        self.dict.add( { "location" : ( "\"%s\"" % location ) } )
        self.dict.add( { "version" : "2.0" } )
        self.dict.add( { "class" : type } )

    def write(self):
        self.dict.write()

    def writeToFile(self, file, indent):
        self.dict.writeToFile(file, indent)

class iodictionary(dictionary):

    def __init__(self, name, objectName, location, typeName):
        self.name = name
        self.object = objectName
        self.location = location
        self.type = typeName
        self.header = header("FoamFile", self.object, self.location, self.type)
        dictionary.__init__(self, self.name)
        
    def write( self, indent ):

        print( openfoamconstants.comment )
        self.header.write()
        print( openfoamconstants.comment )

        numKeys = len(self.entries.items())
        for i in range(numKeys):
            e0 = self.entries.items()[i][0]
            e1 = self.entries.items()[i][1]
            if type(e1) != type(str()):
                e1.write( indent )
            else:
                s = "%-20s %s;\n" % (e0 , e1 )
                print( (s).rjust( indent*4+len(s) ) )
            

        print( openfoamconstants.comment )

    def writeToFile( self, file, indent ):

        file.write( openfoamconstants.comment )
        file.write( "\n\n" )
        self.header.writeToFile(file, indent)
        file.write( "\n" )
        file.write( openfoamconstants.comment )
        file.write( "\n\n" )

        numKeys = len(self.entries.items())
        for i in range(numKeys):
            e0 = self.entries.items()[i][0]
            e1 = self.entries.items()[i][1]
            if type(e1) != type(str()):
                e1.writeToFile( file, indent )
            else:
                s = "%-20s %s;\n" % (e0 , e1 )
                file.write( (s).rjust( indent*4+len(s) ) )
            file.write( "\n" )

        file.write( openfoamconstants.comment )
        file.write( "\n" )
        file.close()


class blockMeshDict(iodictionary):

    def __init__(self):
        self.name = "blockMeshDict"
        self.object = "blockMeshDict"
        self.location = "system"
        self.type = "dictionary"
        iodictionary.__init__(self, self.name, self.object, self.location, self.type)

        self.vertices = list( "vertices" )
        self.blocks = list( "blocks" )
        self.edges = list( "edges" )
        self.patches = list( "patches" )
        self.mergePatchPairs = list( "mergePatchPairs" )

        self.add( { "convertToMeters" : "1.0" } )

        self.add( { self.vertices.name : self.vertices } )
        self.add( { self.blocks.name : self.blocks } )
        self.add( { self.edges.name : self.edges } )
        self.add( { self.patches.name : self.patches } )
        self.add( { self.mergePatchPairs.name : self.mergePatchPairs } )
#   
#    def write( self ):
#        print( openfoamconstants.comment )
#        self.header.write( )
#        print( openfoamconstants.comment )
#        self.vertices.write( 0 )
#        self.blocks.write( 0 )
#        self.edges.write( 0 )
#        self.patches.write( 0 )
#        self.mergePatchPairs.write( 0 )


