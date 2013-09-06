import sys
from socket import *
import select
import marshal

import comm_codes
from controller import Controller
from utils import *

from time import time

################################################################################

RobotCommError = 'RobotcommError'

class RobotComm:
    CONSOLE_PORT = 50000

    def __init__( self, id, host ):
        self.host = host
        self.id = id
        self.queued_msgs = []
        self.console_addr = ( self.host, RobotComm.CONSOLE_PORT )

    def open( self ):
        self.sock = socket( AF_INET, SOCK_DGRAM )
        self.sock.bind( ('', RobotComm.CONSOLE_PORT + self.id) )

    def check_msgs( self, wait_for=None ):
        # make sure we the socket has been opened
        if ( not self.sock ):
            raise RobotCommError, 'need to open robot (%d) comm' % self.id

        # handle any queued messages
        if ( ( not wait_for ) and self.queued_msgs ):
            for msg in self.queued_msgs:
                self.handle_msg( msg )
            self.queued_msgs = []

        # keep going while there's messages waiting
        while ( 1 ):
            # see if there's any messages waiting
            ( i, o, e ) = select.select( [self.sock], [], [], 0.01 )
            if ( not i ):
                break

            # read and handle a message
            ( msg, (host, port) ) = self.sock.recvfrom( 65536 )
            msg = marshal.loads( msg )

            if ( msg[0] == wait_for ):
                return msg
            elif ( wait_for ):
                self.queued_msgs.append( msg )
            else:
                self.handle_msg( msg )

    def wait_for_msg( self, wait_for ):
        msg = None
        while ( not msg ):
            msg = self.check_msgs( wait_for=wait_for )
        return msg

    def handle_msg( self, msg ):
        if ( msg[0] in RobotComm.handlers.keys() ):
            RobotComm.handlers[ msg[0] ]( self, msg )
        else:
            print 'Error: unregistered message number:', msg[0]

    def send_alive_confirmation( self, pos, color,
                                 max_vel, max_angular_vel, radius ):
        s = marshal.dumps( ( comm_codes.ALIVE, self.id,
                             pos.location.x, pos.location.y, pos.location.z,
                             pos.heading, color, max_vel, max_angular_vel,
                             radius ) )
        self.sock.sendto( s, self.console_addr )

    def send_position_update( self, pos ):
        s = marshal.dumps( ( comm_codes.POSITION, self.id,
                             pos.location.x, pos.location.y, pos.location.z,
                             pos.heading ) )
        self.sock.sendto( s, self.console_addr )

    def get_position( self ):
        s = marshal.dumps( ( comm_codes.REQUEST_POSITION, self.id ) )
        self.sock.sendto( s, self.console_addr )
        msg = self.wait_for_msg( comm_codes.POSITION )
        ( type, x, y, z, t ) = msg
        return RobotPosition( Vector( x, y, z ), t )

    def send_death_msg( self ):
        s = marshal.dumps( ( comm_codes.ROBOT_DYING, self.id ) )
        self.sock.sendto( s, self.console_addr )

    def start_robot( self, msg ):
        self.controller.paused = false

    def kill( self, msg ):
        self.send_death_msg()
        self.sock.close()
        sys.exit( -1 )

    def switch_paused( self, msg ):
        self.controller.paused = not self.controller.paused

    def get_obs( self ):
        s = marshal.dumps( ( comm_codes.GET_OBSTACLES, self.id ) )
        self.sock.sendto( s, self.console_addr )
        msg = self.wait_for_msg( comm_codes.OBS_READINGS )

        obstacles = []
        i = 1
        while ( i < len( msg ) ):
            obstacles.append( Vector( msg[i], msg[i+1], 0 ) )
            i = i + 2

        return obstacles

    def sim_move( self, movement ):
        s = marshal.dumps( ( comm_codes.MOVE, self.id,
                             movement.x, movement.y ) )
        self.sock.sendto( s, self.console_addr )

    handlers = { comm_codes.START : start_robot,
                 comm_codes.KILL  : kill,
                 comm_codes.PAUSE : switch_paused }
