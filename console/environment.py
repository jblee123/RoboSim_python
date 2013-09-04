import sys
sys.path.append( '..' )

from utils import *

################################################################################

class Obstacle:
    def __init__( self, x, y, r ):
        self.x = x
        self.y = y
        self.r = r

    def intersect_with_ray( self, ray ):
        intersection = None
        ( x0, y0 ) = ( ray.from_vec.x, ray.from_vec.y )
        ( dx, dy ) = ( ray.to_vec.x - x0, ray.to_vec.y - y0 )
        a = dx**2 + dy**2
        b = 2 * ( x0 * dx - self.x * dx + y0 * dy - self.y * dy )
        c = x0**2 + self.x**2 - 2 * x0 * self.x + y0**2 + self.y**2 - \
            2 * y0 * self.y - self.r**2
        quot = b**2 - 4 * a * c
        if ( quot >= 0 ):
            t1 = ( -b + sqrt( quot ) ) / ( 2 * a )
            t2 = ( -b - sqrt( quot ) ) / ( 2 * a )
            v1 = v2 = None
            if ( t1 >= 0 ):
                v1 = Vector( x0 + t1 * dx, y0 + t1 * dy, 0 )
            if ( t2 >= 0 ):
                v2 = Vector( x0 + t2 * dx, y0 + t2 * dy, 0 )
            if ( v1 and v2 ):
                if ( ( v1 - ray.from_vec ).len() <
                     ( v2 - ray.from_vec ).len() ):
                    intersection = v1
                else:
                    intersection = v2
            elif ( v1 ):
                intersection = v1
            else:
                intersection = v2
        return intersection

################################################################################

class Object:
    def __init__( self, x, y, r, color ):
        self.x = x
        self.y = y
        self.r = r
        self.color = color

################################################################################

class Wall:
    def __init__( self, x1, y1, x2, y2 ):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def intersect_with_ray( self, ray ):
        intersection = None
        ( x0,  y0  ) = ( ray.from_vec.x, ray.from_vec.y )
        ( dxr, dyr ) = ( ray.to_vec.x - x0, ray.to_vec.y - y0 )
        ( dxs, dys ) = ( self.x2 - self.x1, self.y2 - self.y1 )
        if ( ( ( dxs * dyr - dys * dxr ) != 0 ) and
             ( ( dxr != 0 ) or ( dyr != 0 ) ) ):
            ts = dxr * ( self.y1 - y0 ) + dyr * ( x0 - self.x1 )
            ts = ts / ( dxs * dyr - dys * dxr )
            if ( dxr != 0 ):
                tr = ( self.x1 + ts * dxs - x0 ) / dxr
            else:
                tr = ( self.y1 + ts * dys - y0 ) / dyr
            if ( ( ts >= 0 ) and ( ts <= 1 ) and ( tr >= 0 ) ):
                intersection = Vector( self.x1 + ts * dxs, self.y1 + ts * dys )
        return intersection

################################################################################

class Label:
    def __init__( self, x, y, text ):
        self.x = x
        self.y = y
        self.text = text

################################################################################

class EnvironmentScale:
    def __init__( self, w=10, h=10, environment=None ):
        self.original_width_pixel  = w
        self.original_height_pixel = h
        self.env = environment

        self.init_pixels_per_meter()

    def set_original_size( self, w, h ):
        self.original_width_pixel  = w
        self.original_height_pixel = h
        self.init_pixels_per_meter()

    def set_environment( self, env ):
        self.env = env
        self.init_pixels_per_meter()

    def init_pixels_per_meter( self ):
        if ( self.env ):
            pix_per_meter_x = self.original_width_pixel  / self.env.width
            pix_per_meter_y = self.original_height_pixel / self.env.height
            self.pixels_per_meter = min( pix_per_meter_x, pix_per_meter_y )

    def meters_to_pixels( self, x, y ):
        x = x * self.pixels_per_meter
        y = self.pixels_per_meter * self.env.height - \
            ( y * self.pixels_per_meter )
        return ( x, y )

    def env_size_in_pixels( self ):
        ( x, y ) = ( 0, 0 )
        if ( self.env ):
            x = self.pixels_per_meter * self.env.width
            y = self.pixels_per_meter * self.env.height
        return ( x, y )

    def zoom_in( self ):
        self.pixels_per_meter = self.pixels_per_meter * 2

    def zoom_out( self ):
        self.pixels_per_meter = self.pixels_per_meter / 2

################################################################################

class Environment:
    def __init__( self ):
        self.width  = 10 # in meters
        self.height = 10 # in meters

        self.clear_all()

    def add( self, type, item ):
        exec( 'self.%ss.append( item )' % type )

    def clear_all( self ):
        self.obstacles = []
        self.walls     = []
        self.labels    = []
        self.objects   = []

################################################################################

EnvDrawerError = 'EnvDrawerError'

class EnvDrawer:
    def __init__( self, canvas=None, env=None, scale=None ):
        self.canvas = canvas
        self.env = env
        self.scale = scale

        self.robot_ids = {}

    def set_environment( self, env ):
        self.env = env

    def draw_env( self ):
        if ( not self.canvas ):
            raise EnvDrawerError, 'canvas is missing'

        if ( not self.env ):
            raise EnvDrawerError, 'env is missing'

        if ( not self.scale ):
            raise EnvDrawerError, 'scale is missing'

        for x in self.env.obstacles:
            self.draw_obstacle( x )

        for x in self.env.walls:
            self.draw_wall( x )

        for x in self.env.labels:
            self.draw_label( x )

        for x in self.env.objects:
            self.draw_object( x )

    def draw_obstacle( self, obs ):
        ( x, y ) = self.scale.meters_to_pixels( obs.x, obs.y )
        r = self.scale.meters_to_pixels( obs.r, 0 )[0]
        self.canvas.create_oval( x-r, y-r, x+r, y+r, fill='black' )

    def draw_wall( self, wall ):
        ( x1, y1 ) = self.scale.meters_to_pixels( wall.x1, wall.y1 )
        ( x2, y2 ) = self.scale.meters_to_pixels( wall.x2, wall.y2 )
        self.canvas.create_line( x1, y1, x2, y2, fill='black' )

    def draw_label( self, label ):
        pass

    def draw_object( self, obj ):
        ( x, y ) = self.scale.meters_to_pixels( obj.x, obj.y )
        r = self.scale.meters_to_pixels( obj.r, 0 )[0]
        self.canvas.create_oval( x-r, y-r, x+r, y+r, fill=obj.color, outline=obj.color )

    def draw_readings( self, readings ):
        self.canvas.delete( 'obs_reading' )
        for reading in readings:
            ( x, y ) = self.scale.meters_to_pixels( reading.x, reading.y )
            self.canvas.create_oval( x-2, y-2, x+2, y+2,
                                     outline='red', tag='obs_reading' )

    def draw_robot( self, x, y, t, color='blue', id=None ):
        point1 = Vector( -0.5,  0.5 )
        point2 = Vector(  0.5,  0.5 )
        point3 = Vector(  1.0,  0.0 )
        point4 = Vector(  0.5, -0.5 )
        point5 = Vector( -0.5, -0.5 )

        p = Vector( x, y )
        point1 = point1.rotate_z( t ) + p
        point2 = point2.rotate_z( t ) + p
        point3 = point3.rotate_z( t ) + p
        point4 = point4.rotate_z( t ) + p
        point5 = point5.rotate_z( t ) + p
        ( x1, y1 ) = self.scale.meters_to_pixels( point1.x, point1.y )
        ( x2, y2 ) = self.scale.meters_to_pixels( point2.x, point2.y )
        ( x3, y3 ) = self.scale.meters_to_pixels( point3.x, point3.y )
        ( x4, y4 ) = self.scale.meters_to_pixels( point4.x, point4.y )
        ( x5, y5 ) = self.scale.meters_to_pixels( point5.x, point5.y )

        if ( id and ( id in self.robot_ids.keys() ) ):
            self.canvas.delete( self.robot_ids[ id ] )

        obj_id = self.canvas.create_polygon( x1, y1, \
                                             x2, y2, \
                                             x3, y3, \
                                             x4, y4, \
                                             x5, y5, \
                                             fill=color )
        self.robot_ids[ id ] = obj_id
        self.canvas.update()

    def erase_robot( self, id ):
        self.canvas.delete( self.robot_ids[ id ] )
        del self.robot_ids[ id ]
