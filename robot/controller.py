import sys

from behaviors.behavior_imports import *

import time
import logger

################################################################################

class Controller:
    def __init__( self, behaviors_to_run=[] ):
        self.communicator = None
        self.behaviors_to_run = behaviors_to_run
        self.paused = true

    def add_behavior( self, to_add ):
        self.behaviors_to_run.append( to_add )

    def get_robot_instance( self ):
        return robot.Robot.robot_instance

    def set_paused( self, paused ):
        self.paused = paused

    def run( self ):
        # make sure all the behaviors are connected up
        for behavior in self.get_robot_instance().behaviors.values():
            behavior.connect_inputs()

        while ( true ):
            # check for msgs
            self.get_robot_instance().communicator.check_msgs()

            # don't do anything if we're paused
            if ( self.paused ):
                continue

            # run all the top-level behaviors
            for behavior in self.behaviors_to_run:
                behavior.get_output()

            self.get_robot_instance().increment_cycle()

################################################################################
