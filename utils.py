from math import *

################################################################################

true  = 1
false = 0

################################################################################

def deg_to_rad( deg ):
    return deg * ( ( 2 * pi ) / 360 )

################################################################################

def rad_to_deg( rad ):
    return rad * ( 360 / ( 2 * pi ) )

################################################################################

def normalize_angle( angle ):
    while ( angle < 0 ):
        angle = angle + 360

    while ( angle >= 360 ):
        angle = angle - 360

    return angle

################################################################################

class Vector:
    def __init__( self, x=0, y=0, z=0, data=None ):
        if ( data != None ):
            self.x = data.x
            self.y = data.y
            self.z = data.z
        else:
            self.x = x
            self.y = y
            self.z = z

    def clone( self ):
        return Vector( data=self )

    def __str__( self ):
        return '(%.02f, %.02f, %.02f)' % (self.x, self.y, self.z)

    def __eq__( self, other ):
        return ( other and \
                 ( self.x == other.x ) and \
                 ( self.y == other.y ) and \
                 ( self.z == other.z ) )

    def __ne__( self, other ):
        return not self.__eq__( other )

    def __add__( self, other ):
        return Vector( self.x + other.x, self.y + other.y, self.z + other.z )

    def __sub__( self, other ):
        return Vector( self.x - other.x, self.y - other.y, self.z - other.z )

    def __mul__( self, num ):
        return Vector( self.x * num, self.y * num, self.z * num )

    def __div__( self, num ):
        return Vector( self.x / num, self.y / num, self.z / num )

    def rotate_z( self, amount ):
        c = cos( deg_to_rad( amount ) )
        s = sin( deg_to_rad( amount ) )
        x = self.x
        y = self.y
        self.x = x * c - y * s
        self.y = x * s + y * c
        return self

    def get_angle( self ):
        return normalize_angle( rad_to_deg( atan2( self.y, self.x ) ) )

    def len( self ):
        return sqrt( self.x**2 + self.y**2 + self.z**2 )

    def get_unit( self ):
        if ( self.len() == 0 ):
            return Vector( 1, 0, 0 )
        else:
            return self / self.len()

################################################################################

class RobotPosition:
    def __init__( self, location=None, heading=0 ):
        self.location = Vector( data=location )
        self.heading  = heading

    def __str__( self ):
        s1 = str(self.location)
        a = self.heading * 1
        s2 = '%f' % (self.heading * 1.0)
        return '[%s, %f]' % ( s1, self.heading )

    def clone( self ):
        return RobotPosition( location=self.location, heading=self.heading )

################################################################################

class Ray:
    def __init__( self, from_vec=None, to_vec=None ):
        self.from_vec = from_vec
        if ( from_vec ): self.from_vec = from_vec.clone()

        self.to_vec = to_vec
        if ( to_vec ): self.to_vec = to_vec.clone()

    def intersect_with_circle( self, xc, yc, r ):
        intersection = None
        ( x0, y0 ) = ( self.from_vec.x, self.from_vec.y )
        ( dx, dy ) = ( self.to_vec.x - x0, self.to_vec.y - y0 )
        a = dx**2 + dy**2
        b = 2 * ( x0 * dx - xc * dx + y0 * dy - yc * dy )
        c = x0**2 + xc**2 - 2 * x0 * xc + y0**2 + yc**2 - 2 * y0 * yc - r**2
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
                if ( ( v1 - self.from_vec ).len() <
                     ( v2 - self.from_vec ).len() ):
                    intersection = v1
                else:
                    intersection = v2
            elif ( v1 ):
                intersection = v1
            else:
                intersection = v2
        return intersection

    def intersect_with_segment( self, xs0, ys0, xs1, ys1 ):
        intersection = None
        ( x0,  y0  ) = ( self.from_vec.x, self.from_vec.y )
        ( dxr, dyr ) = ( self.to_vec.x - x0, self.to_vec.y - y0 )
        ( dxs, dys ) = ( xs1 - xs0, ys1 - ys0 )
        if ( ( ( dxs * dyr - dys * dxr ) != 0 ) and
             ( ( dxr != 0 ) or ( dyr != 0 ) ) ):
            ts = dxr * ( ys0 - y0 ) + dyr * ( x0 - xs0 )
            ts = ts / ( dxs * dyr - dys * dxr )
            if ( dxr != 0 ):
                tr = ( xs0 + ts * dxs - x0 ) / dxr
            else:
                tr = ( ys0 + ts * dys - y0 ) / dyr
            if ( ( ts >= 0 ) and ( ts <= 1 ) and ( tr >= 0 ) ):
                intersection = Vector( xs0 + ts * dxs, ys0 + ts * dys )
        return intersection
