from behavior_imports import *

AvoidObsError = 'AvoidObsError'

################################################################################
#
# Inputs: tuple of Vectors obs_list
#         literal scalar safety_margin
#
################################################################################

class AvoidObs(Behavior):
    def __init__( self, name=None, obs_list=None, \
                  safety_margin=None, sphere_of_influence=None ):
        Behavior.__init__( self, name )
        self.obs_list = obs_list
        self.safety_margin = safety_margin
        self.sphere_of_influence = sphere_of_influence

################################################################################

    def compute_output( self ):
        if ( self.obs_list == None ):
            raise AvoidObsError, 'obs_list input not set'

        if ( self.safety_margin == None ):
            raise AvoidObsError, 'safety_margin input not set'

        if ( self.sphere_of_influence == None ):
            raise AvoidObsError, 'sphere_of_influence input not set'

        obstacles = self.obs_list.get_output()
        self.output = Vector( 0, 0, 0 )
        for obs in obstacles:
            length = obs.len()
            if ( length < self.sphere_of_influence.get_output() ):
                if ( length < self.safety_margin.get_output() ):
                    obs = obs * 100000
                self.output = self.output + ( obs * -1 )
