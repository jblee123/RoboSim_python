from behavior_imports import *

################################################################################

class Behavior:
    next_id = 1
    def __init__( self, name=None ):
        self.name = name
        if name == None:
            self.name = 'AN_%s' % Behavior.next_id
            Behavior.next_id = Behavior.next_id + 1

        self.get_robot().behaviors[ self.name ] = self

        self.output = None
        self.last_cycle = -2

################################################################################

    def get_robot( self ):
        return robot.Robot.robot_instance

################################################################################

    def get_robot_interface( self ):
        return self.get_robot() and self.get_robot().interface

################################################################################

    def connect_inputs( self ):
        pass

################################################################################

    def setVal( self, var_name, value ):
        exec( 'self.%s = value' % var_name )

################################################################################

    def activate( self ):
        pass

################################################################################

    def compute_output( self ):
        self.output = 0

################################################################################

    def get_output( self ):
        cycle_num = self.get_robot().get_cycle()

        if ( ( cycle_num - self.last_cycle ) > 2 ):
            self.activate()

        if ( self.last_cycle < cycle_num ):
            self.compute_output()
            self.last_cycle = cycle_num

        return self.output
