import sys

from behaviors.behavior_imports import *
from robot_interfaces.sim_robot_interface import *
from controller import *
from robot_comm import *

################################################################################

class Robot:
    robot_instance = None

    def __init__( self,
                  id,
                  host='localhost',
                  type='simulation',
                  x_pos=1,
                  y_pos=1,
                  theta=0,
                  color='blue',
                  max_vel=-1,
                  max_angular_vel=-1,
                  radius=0.5 ):
        Robot.robot_instance = self

        self.cycle_num = 0
        self.behaviors = {}

        self.id = id
        self.host = host
        self.color = color
        self.max_vel = max_vel
        self.max_angular_vel = max_angular_vel
        self.radius = radius

        # set up the robot type
        if ( type == 'simulation' ):
            self.interface = SimRobotInterface()
        else:
            print "Error: robot type '%s' not currently supported" % type
            sys.exit( -1 )

        pos = RobotPosition( Vector( x_pos, y_pos ), theta )

        # init communication back to the console
        self.communicator = RobotComm( id, host )
        self.communicator.open()
        self.communicator.send_alive_confirmation(
            pos, color, max_vel, max_angular_vel, radius )

        self.controller = Controller()

        # link the controller and communicator to each other
        self.controller.communicator = self.communicator
        self.communicator.controller = self.controller

        self.interface.communicator = self.communicator
        self.interface.set_position( pos )

    def get_cycle( self ):
        return self.cycle_num

    def increment_cycle( self ):
        self.cycle_num = self.cycle_num + 1

    def add_behavior( self, behavior ):
        self.controller.add_behavior( behavior )

    def run( self ):
        self.controller.run()
