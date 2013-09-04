import sys, os, inspect

f = inspect.currentframe()

print inspect.getframeinfo( f )

print inspect.getfile( f )

print os.path.dirname( inspect.getfile( f ) )

print os.path.split( os.path.dirname( inspect.getfile( f ) ) )

print os.path.split( inspect.getfile( f ) )

print os.path.join( os.path.dirname( inspect.getfile( f ) ), 'asdf' )

#print os.path.dirname( os.path.split( inspect.getfile( f ) ) )

print os.getcwd()