import os, sys

if ( sys.platform[:3] == 'win' ):
    pypath = r'C:\program files\python22\python.exe'
    robot_path = r'D:\code\python\RoboSim\robot\robot_test.py'
    os.spawnv( os.P_NOWAIT, pypath, ( 'python', robot_path ) )
else:
    print ( 'os (%s) not supported yet' % (sys.platform) )
