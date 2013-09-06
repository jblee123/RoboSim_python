import sys
sys.path.append( '..' )

from utils import *
from robot_interface import *

import logger

################################################################################

class SimRobotInterface(RobotInterface):
    def __init__( self ):
        RobotInterface.__init__( self )
        self.position = RobotPosition()
        self.communicator=None

    def get_position( self ):
        return self.communicator.get_position()

    def set_position( self, new_pos ):
        self.communicator.send_position_update( new_pos )

    def move( self, movement ):
        self.communicator.sim_move( movement )

    def get_obs_readings( self ):
        return self.communicator.get_obs()
