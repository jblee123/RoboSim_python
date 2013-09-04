import sys, os, inspect

base_dir = os.path.dirname( inspect.getfile( inspect.currentframe() ) )
base_dir = os.path.dirname( os.path.realpath( base_dir ) )
if ( base_dir not in sys.path ):
    sys.path.append( base_dir )

import getopt

from robot import Robot
from behaviors.behavior_imports import *

################################################################################

def print_usage():
    usage = """-i <robot_id> [-h <host>]"""
    print 'usage: %s %s' % ( sys.argv[0], usage )

################################################################################

# get command line args
optlist = 0
args    = 0

try:
    optlist, args = getopt.getopt( sys.argv[1:], 'i:h:T:x:y:t:c:v:a:r:' )
except getopt.error, what:
    print what
    print_usage()
    sys.exit( -1 )

id = 1
host = 'localhost'
type = 'simulation'
x_pos = 1
y_pos = 1
theta = 0
color = 'blue'
max_vel = -1
max_angular_vel = -1
radius = 0.5

for opt in optlist:
    if ( opt[0] == '-i' ):
        id = int( opt[1] )
    elif ( opt[0] == '-h' ):
        host = opt[1]
    elif ( opt[0] == '-T' ):
        type = opt[1]
    elif ( opt[0] == '-x' ):
        x_pos = float( opt[1] )
    elif ( opt[0] == '-y' ):
        y_pos = float( opt[1] )
    elif ( opt[0] == '-t' ):
        theta = float( opt[1] )
    elif ( opt[0] == '-c' ):
        color = opt[1]
    elif ( opt[0] == '-v' ):
        max_vel = float( opt[1] )
    elif ( opt[0] == '-a' ):
        max_angular_vel = float( opt[1] )
    elif ( opt[0] == '-r' ):
        radius = float( opt[1] )
    else:
        print 'Error: bad option:', opt[0]
        print_usage()
        sys.exit( -1 )


r = Robot( id=id, host=host, type=type,
           x_pos=x_pos, y_pos=y_pos, theta=theta, color=color,
           max_vel=max_vel, max_angular_vel=max_angular_vel, radius=radius )

r.add_behavior( TestGoto() )
r.run()
