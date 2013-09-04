from behavior_imports import *

GlobalToEgocentricError = 'GlobalToEgocentricError'

################################################################################
#
# Inputs: RobotPosition robot_pos
#         Vector global_pos
#
################################################################################

class GlobalToEgocentric(Behavior):
    def __init__( self, name=None, robot_pos=None, global_pos=None ):
        Behavior.__init__( self, name )
        self.robot_pos  = robot_pos
        self.global_pos = global_pos

################################################################################

    def compute_output( self ):
        if ( self.robot_pos == None ):
            raise GlobalToEgocentricError, 'robot_pos input not set'

        if ( self.global_pos == None ):
            raise GlobalToEgocentricError, 'global_pos input not set'

        robot_pos = self.robot_pos.get_output()
        global_pos = self.global_pos.get_output()

        self.output = global_pos - robot_pos.location
        self.output.rotate_z( robot_pos.heading * -1 )
