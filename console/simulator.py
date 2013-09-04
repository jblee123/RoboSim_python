import sys

from utils       import *
import environment
from environment import *

import time

################################################################################

class RobotInfo:
    def __init__( self, pos=None, color='blue',
                  max_vel=-1, max_angular_vel=-1, radius=0.5 ):
        self.pos = pos or RobotPosition( Vector( 0, 0, 0 ), 0 )
        self.color = color
        self.max_vel = max_vel
        self.max_angular_vel = max_angular_vel
        self.radius = radius

################################################################################

class Simulator:
    NUM_OF_SIM_RAYS = 16

    def __init__( self, app_instance=None, time_step=0.2 ):
        self.app_instance = app_instance
        self.time_step = time_step
        self.robots = {}

    def register_robot( self, id, pos, color,
                        max_vel, max_angular_vel, radius ):
        self.robots[ id ] = RobotInfo( pos, color,
                                       max_vel, max_angular_vel, radius )
        self.app_instance.communicator.send_start_msg( id )

    def update_robot_pos( self, id, pos ):
        if ( id in self.robots.keys() ):
            robot = self.robots[ id ]
            robot.pos = pos
            self.app_instance.console.env_drawer.draw_robot( \
                pos.location.x, pos.location.y, pos.heading, robot.color, id )
        else:
            print 'Error: tried to update an unregistered robot:', id

    def get_robot_pos( self, id ):
        pos = None
        if ( id in self.robots.keys() ):
            pos = self.robots[ id ].pos
        else:
            print 'Error: tried to get the position of an unregistered robot:', id
        return pos

    def global_to_egocentric( self, robot_pos, to_convert ):
        pos = to_convert - robot_pos.location
        pos.rotate_z( robot_pos.heading * -1 )
        return pos

    def egocentric_to_global( self, robot_pos, to_convert ):
        pos = to_convert.clone().rotate_z( robot_pos.heading )
        pos = to_convert + robot_pos.location
        return pos

    def get_closest_reading( self, robot, ray_num ):
        # create the ray_num'th ray
        v = Vector( 1, 0, 0 )
        ray_angle = ray_num * 360 / Simulator.NUM_OF_SIM_RAYS
        v.rotate_z( robot.pos.heading + ray_angle )
        v = v + robot.pos.location
        ray = Ray( robot.pos.location, v )

        # get the closest intersection
        closest_dist = 1000000
        closest_reading = None

        # look for the closest reading
        env = self.app_instance.environment
        for obs in ( env.obstacles + env.walls ):
            # get the reading depending on the obstacle type
            reading = obs.intersect_with_ray( ray )

            # see if the current obstacle produces the closest reading so far
            if ( reading ):
                reading = self.global_to_egocentric( robot.pos, reading )
                dist = reading.len()
                if ( dist < closest_dist ):
                    closest_dist = dist
                    closest_reading = reading

        return closest_reading

    def get_obs_readings( self, id ):
        readings = []
        if ( id in self.robots.keys() ):
            robot = self.robots[ id ]
            for i in range( Simulator.NUM_OF_SIM_RAYS ):
                 reading = self.get_closest_reading( robot, i )
                 if ( reading ):
                     readings.append( reading )

            to_draw = []
            for r in readings:
                to_draw.append( r.clone().rotate_z( robot.pos.heading ) + \
                                robot.pos.location )
            self.app_instance.console.env_drawer.draw_readings( to_draw )

        return readings

#    def get_obs_readings2( self, id ):
#        readings = []
#        if ( id in self.robots.keys() ):
#            robot = self.robots[ id ]
#            for obs in self.app_instance.environment.obstacles:
#                reading = Vector( obs.x, obs.y, 0 )
#                neg = ( reading * -1 ).get_unit() * obs.r
#                reading = reading - neg
#                reading = reading - robot.pos.location
#                reading.rotate_z( robot.pos.heading * -1 )
#                readings.append( reading )
#        else:
#            print 'Error: tried to get obs readings for an unregistered robot:', id
#
#        return readings

    def robot_dying( self, id ):
        self.app_instance.console.env_drawer.erase_robot( id )
        del self.robots[ id ]
        if ( self.app_instance.shutting_down and ( not self.robots.keys() ) ):
            self.app_instance.exit_robo_sim()

    def constrain_by_robot( self, requested, robot ):
        max_turn = robot.max_angular_vel * self.time_step
        angle = requested.get_angle()
        if ( angle < 180 ):
            angle = min( angle * self.time_step, max_turn )
        else:
            angle = max( ( angle - 360 ) * self.time_step, -max_turn )
        dist = min( robot.max_vel * self.time_step,
                    requested.len() * self.time_step )
        return Vector( dist, 0, 0 ).rotate_z( angle )

    def constrain_by_environment( self, from_vec, to_vec, radius ):
        ray = Ray( from_vec, to_vec )
        delta = to_vec - from_vec
        ray_len = delta.len()

        closest_dist = 1000000
        closest_intersection = None

        # look in the obstacles for the closest reading
        env = self.app_instance.environment
        for obs in ( env.obstacles + env.walls ):
            # get the intersection depending on the obstacle type
            intersection = obs.intersect_with_ray( ray )

            # see if the current obstacle produces the closest
            #  intersection so far
            if ( intersection ):
                intersection_dist = ( intersection - from_vec ).len()
                if ( ( intersection_dist < ( ray_len + radius ) ) and
                     ( intersection_dist < closest_dist ) ):
                    closest_dist = intersection_dist
                    closest_intersection = intersection

        # if the robot's movement intersects an obstacle, produce a
        #  movement vector that stops short of that obstacle
        if ( closest_intersection ):
            delta = delta.get_unit() * ( closest_dist - radius )

        return delta

    def move_robot( self, id, x, y ):
        if ( id in self.robots.keys() ):
            robot = self.robots[ id ]
            requested = Vector( x, y, 0 )

            # make sure the robot doesn't violate max velocity and
            # angular velocity constraints
            v = self.constrain_by_robot( requested, robot )

            v.rotate_z( robot.pos.heading )    # switch to real-world direction
            robot.pos.heading = v.get_angle()  # we've already got the new heading

            # make sure the robot doesn't violate any environmental constraints
            v = self.constrain_by_environment(
                robot.pos.location, robot.pos.location + v, robot.radius )

            # update the robot's position and re-draw it
            robot.pos.location = robot.pos.location + v
            self.app_instance.console.env_drawer.draw_robot(
                robot.pos.location.x, robot.pos.location.y,
                robot.pos.heading, robot.color, id )
        else:
            print 'Error: tried to move an unregistered robot:', id

    def spin_robot( self, id, theta ):
        if ( id in self.robots.keys() ):
            pos = self.robots[ id ]
        else:
            print 'Error: tried to spin an unregistered robot:', id
