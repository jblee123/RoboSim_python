from behavior_imports import *

MoveRobotError = 'MoveRobotError'

################################################################################
#
# Inputs: Vector movement
#
################################################################################

class MoveRobot(Behavior):
    def __init__( self, name=None, \
                  movement=None, base_speed=None, max_speed=None ):
        Behavior.__init__( self, name )
        self.movement = movement
        self.base_speed = base_speed
        self.max_speed = max_speed

################################################################################

    def compute_output( self ):
        if ( self.get_robot_interface() == None ):
            raise MoveRobotError, 'no robot interface'

        if ( self.movement == None ):
            raise MoveRobotError, 'movement input not set'

        vec = self.movement.get_output() * self.base_speed.get_output()
        if ( vec.len() > self.max_speed.get_output() ):
            vec = vec.get_unit() * self.max_speed.get_output()

        self.get_robot_interface().move( vec )
