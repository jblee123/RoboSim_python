import random

from behavior_imports import *

WanderError = 'WanderError'

################################################################################
#
# Inputs: integer persistence
#
################################################################################

class Wander(Behavior):
    def __init__( self, name=None, persistence=None ):
        Behavior.__init__( self, name )
        self.persistence = persistence
        self.same_direction_count = 0

################################################################################

    def compute_output( self ):
        if ( self.persistence == None ):
            raise WanderError, 'persistence input not set'

        if ( self.same_direction_count >= self.persistence.get_output() ):
            self.same_direction_count = 0

        if ( self.same_direction_count == 0 ):
            self.output = Vector( 1, 0, 0 )
            self.output.rotate_z( random.random() * 360 )

        self.same_direction_count = self.same_direction_count + 1

