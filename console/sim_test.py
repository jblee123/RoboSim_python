import console
from environment import *
print '******************'
e = Environment()
e.width  = 50
e.height = 50
e.add( 'obstacle', Obstacle( 10,  5, 1 ) )
e.add( 'obstacle', Obstacle( 15, 10, 2 ) )
e.add( 'obstacle', Obstacle( 20, 15, 3 ) )
e.add( 'wall',     Wall( 1, 1, 10, 1 ) )
e.add( 'object',   Object( 15, 1,  1, 'red' ) )

c = console.Console()
c.set_environment( e )
c.env_drawer.draw_env()

c.mainloop()
