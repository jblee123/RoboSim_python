# import sys, os, inspect

# ################################################################################

# def maybe_append( dir ):
#     if ( dir not in sys.path ):
#         sys.path.append( dir )

# ################################################################################

# #ROBOSIM_DIR = r'd:\code\python\RoboSim'
# #ROBOSIM_DIR = r'/home/blee/d_drive/code/python/RoboSim'
# robosim_dir = os.path.dirname( inspect.getfile( inspect.currentframe() ) )
# print 'robosim_dir: ' + robosim_dir

# subdirs = ( 'console',
#             'robot',
#             os.path.join( 'robot', 'behaviors' ),
#             os.path.join( 'robot', 'robot_interfaces' ) )
# #            r'robot\behaviors',
# #            r'robot\robot_interfaces' )

# maybe_append( robosim_dir )
# for dir in subdirs:
#     #maybe_append( '%s\%s' % ( ROBOSIM_DIR, dir ) )
#     maybe_append( os.path.join( robosim_dir, dir ) )
