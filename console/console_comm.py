from socket import *
import select
import string
import sys
import marshal

from utils import *
import comm_codes

from time import time

################################################################################

ConsoleCommError = 'ConsoleCommError'

class ConsoleComm:
    CONSOLE_PORT = 50000

    def __init__( self, app_instance=None ):
        self.app_instance = app_instance
        self.sock = None

        self.addresses = {}

    def open( self ):
        self.sock = socket( AF_INET, SOCK_DGRAM )
        self.sock.bind( ('', ConsoleComm.CONSOLE_PORT) )

    def check_for_msgs( self ):
        # make sure we the socket has been opened
        if ( not self.sock ):
            raise ConsoleCommError, 'need to open console comm'

        # keep going while there's messages waiting
        while ( 1 ):
            # see if there's any messages waiting
            ( i, o, e ) = select.select( [self.sock], [], [], 0 )
            if ( not i ):
                break

            # read and handle a message
            ( msg, (host, port) ) = self.sock.recvfrom( 65536 )
            print( 'c recv: ' + str(time()))
            msg = marshal.loads( msg )
            if ( msg[0] == comm_codes.ALIVE ):
                self.register_new_robot( msg, (host, port) )
            else:
                self.handle_msg( msg )

        # tell the console to check for messages again later
        if ( self.app_instance and self.app_instance.console ):
            self.app_instance.console.after( 1, self.check_for_msgs )

    def register_new_robot( self, msg, address ):
        ( type, id, x, y, z, t, color, max_vel, max_angular_vel, radius ) = msg

        pos = RobotPosition( Vector( x, y, z ), t )

        # see if we've already registered this ID
        if ( id in self.addresses.keys() ):
            print 'Error: ID', id, 'is being re-used'
            sys.exit( -1 )

        # register the ID
        self.addresses[ id ] = address
        self.app_instance.simulator.register_robot(
            id, pos, color, max_vel, max_angular_vel, radius )
        print 'registered address for ID', id

    def handle_msg( self, msg ):
        if ( msg[0] in ConsoleComm.handlers.keys() ):
            ConsoleComm.handlers[ msg[0] ]( self, msg )
        else:
            print 'Error: unregistered message number:', msg[0]

    def update_robot_pos( self, msg ):
        ( type, id, x, y, z, t ) = msg
        pos = RobotPosition( Vector( x, y, z ), t )
        self.app_instance.simulator.update_robot_pos( id, pos )

    def get_robot_pos( self, msg ):
        ( type, id ) = msg
        pos = self.app_instance.simulator.get_robot_pos( id )
        if ( pos ):
            s = marshal.dumps( (comm_codes.POSITION, pos.location.x,
                                pos.location.y, pos.location.z, pos.heading) )
            print( 'c send: ' + str(time()))
            self.sock.sendto( s, self.addresses[ id ] )

    def send_start_msg( self, id ):
        s = marshal.dumps( (comm_codes.START, ) )
        print( 'c send: ' + str(time()))
        self.sock.sendto( s, self.addresses[ id ] )

    def send_killall( self ):
        s = marshal.dumps( (comm_codes.KILL, ) )
        for address in self.addresses.values():
            print( 'c send: ' + str(time()))
            self.sock.sendto( s, address )

    def send_switch_pause( self ):
        s = marshal.dumps( (comm_codes.PAUSE, ) )
        for address in self.addresses.values():
            print( 'c send: ' + str(time()))
            self.sock.sendto( s, address )

    def get_obs_readings( self, msg ):
        id = msg[1]
        readings = self.app_instance.simulator.get_obs_readings( id )
        data = [ comm_codes.OBS_READINGS, ]
        for reading in readings:
            data.append( reading.x )
            data.append( reading.y )
        data = marshal.dumps( data )
        print( 'c send: ' + str(time()))
        self.sock.sendto( data, self.addresses[ id ] )

    def robot_dying( self, msg ):
        id = msg[1]
        del self.addresses[id]
        self.app_instance.simulator.robot_dying( id )

    def move_robot( self, msg ):
        ( type, id, x, y ) = msg
        self.app_instance.simulator.move_robot( id, x, y )

    def spin_robot( self, msg ):
        ( type, id, theta ) = msg
        self.app_instance.simulator.spin_robot( id, theta )

    handlers = { comm_codes.POSITION         : update_robot_pos,
                 comm_codes.REQUEST_POSITION : get_robot_pos,
                 comm_codes.GET_OBSTACLES    : get_obs_readings,
                 comm_codes.ROBOT_DYING      : robot_dying,
                 comm_codes.MOVE             : move_robot,
                 comm_codes.SPIN             : spin_robot }
