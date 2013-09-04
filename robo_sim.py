import sys, os
from subprocess import Popen
import Tkinter

from console.console      import Console
from console.simulator    import Simulator
from console.console_comm import ConsoleComm
from console.environment  import *
from utils        import *

################################################################################

class RoboSim:
    def __init__( self ):
        self.console = Console( parent=Tkinter.Tk(), app_instance=self )

        self.shutting_down = false

        self.simulator = Simulator( app_instance=self )

        self.environment = Environment()

        self.communicator = ConsoleComm( app_instance=self )
        self.communicator.open()
        self.communicator.check_for_msgs()

    def run_mainloop( self ):
        self.console.mainloop()

    def killapp( self ):
        sys.exit( -1 )

    def set_environment( self, env ):
        self.environment = env
        self.console.update_environment( env )

    def exit_robo_sim( self ):
        self.console.destroy()
        sys.exit()

    def initiate_shutdown( self ):
        self.shutting_down = true
        self.communicator.send_killall()
        self.console.after( 1000, self.exit_robo_sim )

################################################################################
RUN_ANYWAY = 0
if ( RUN_ANYWAY or ( __name__ == '__main__' ) ):
    e = Environment()
    e.width  = 50
    e.height = 50
#    e.add( 'obstacle', Obstacle(  5,  5, 1 ) )
    e.add( 'obstacle', Obstacle( 10, 10, 2 ) )
    e.add( 'obstacle', Obstacle( 15, 15, 3 ) )
    e.add( 'wall',     Wall( 15, 35, 25, 35 ) )
    e.add( 'wall',     Wall( 25, 35, 35, 25 ) )
##    e.add( 'wall',     Wall( 35, 25, 35, 15 ) )
    e.add( 'object',   Object( 49, 49,  1, 'red' ) )

#    e.add( 'wall', Wall( 15, 15, 15, 35 ) )
#    e.add( 'wall', Wall( 15, 35, 35, 35 ) )
#    e.add( 'wall', Wall( 35, 35, 35, 15 ) )
#    e.add( 'wall', Wall( 35, 15, 15, 15 ) )

    app = RoboSim()
    app.set_environment( e )

    #pypath = r'C:\program files\python23\python.exe'
    #robot_path = r'D:\code\python\RoboSim\robot\robot_test.py'
    #pypath = r'/usr/bin/'
    #robot_path = r'/home/blee/d_drive/code/python/RoboSim/robot/robot_test.py'

    # robot_path = os.path.join( os.path.dirname( inspect.getfile( inspect.currentframe() ) ), 'robot', 'robot_test.py' )
    # print 'robot_path: ' + robot_path

    # os.spawnv( os.P_NOWAIT, pypath, \
    #            ( 'python', robot_path,
    #              '-i', '1', '-x', '1', '-y', '1', '-c', 'blue', '-v', '1', '-a', '20' ) )
    Popen( [ 'python', os.path.join( 'robot', 'robot_test.py' ),
             '-i', '1', '-x', '1', '-y', '1', '-c', 'blue', '-v', '1', '-a', '20' ] )


#    pid = os.fork()
#    if ( pid == 0 ):
#        os.execv( pypath, ( 'python', robot_path,
#                 '-i', '1', '-x', '1', '-y', '1', '-c', 'blue', '-v', '1', '-a', '20' ) )

#    os.spawnv( os.P_NOWAIT, pypath, \
#               ( 'python', robot_path, '-i', '2', '-x', '40', '-y', '40', '-c', 'red' ) )
#    os.spawnv( os.P_NOWAIT, pypath, \
#               ( 'python', robot_path, '-i', '3', '-x', '40', '-y', '1', '-c', 'green' ) )
#    os.spawnv( os.P_NOWAIT, pypath, \
#               ( 'python', robot_path, '-i', '4', '-x', '1', '-y', '40', '-c', 'orange' ) )

    app.run_mainloop()
