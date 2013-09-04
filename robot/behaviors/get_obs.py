from behavior_imports import *

GetObsError = 'GetObsError'

################################################################################
#
# Inputs:
#
################################################################################

class GetObs(Behavior):
    def __init__( self, name=None ):
        Behavior.__init__( self, name )

################################################################################

    def compute_output( self ):
        self.output = self.get_robot_interface().get_obs_readings()
