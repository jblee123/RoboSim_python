from behavior_imports import *

LiteralError = 'LiteralError'

################################################################################

class Literal(Behavior):
    def __init__( self, val=None, name=None  ):
        Behavior.__init__( self, name )
        if ( val != None ):
            self.output = val

################################################################################

    def compute_output( self ):
        if ( self.output == None ):
            raise LiteralError, 'output not set'
