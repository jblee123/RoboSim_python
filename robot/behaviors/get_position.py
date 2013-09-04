from behavior_imports import *

GetPositionError = 'GetPositionError'

################################################################################

class GetPosition(Behavior):
    def __init__( self, name=None  ):
        Behavior.__init__( self, name )

################################################################################

    def compute_output( self ):
        if ( self.get_robot_interface() == None ):
            raise GetPositionError, 'no robot interface'

        self.output = self.get_robot_interface().get_position()
