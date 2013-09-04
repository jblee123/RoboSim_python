from behavior_imports import *

MoveToError = 'MoveToError'

################################################################################
#
# Inputs: Vector target
#
################################################################################

class MoveTo(Behavior):
    def __init__( self, name=None, target=None ):
        Behavior.__init__( self, name )
        self.target = target

################################################################################

    def compute_output( self ):
        if ( self.target == None ):
            raise MoveToError, 'target input not set'

        self.output = self.target.get_output().get_unit()
