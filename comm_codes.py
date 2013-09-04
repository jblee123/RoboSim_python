msgs = ( 'ALIVE',
         'START',
         'REQUEST_POSITION',
         'POSITION',
         'KILL',
         'ROBOT_DYING',
         'GET_OBSTACLES',
         'OBS_READINGS',
         'PAUSE',
         'MOVE',
         'SPIN' )

i = 0
while ( i < len(msgs) ):
    exec( '%s = %d' % ( msgs[i], i ) )
    i = i + 1
