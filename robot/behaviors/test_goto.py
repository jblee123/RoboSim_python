from behavior_imports import *
#from avoid_obs        import *
#from get_obs          import *

################################################################################

class TestGoto(Behavior):
    def __init__( self, name=None ):
        Behavior.__init__( self, name )

        self.move_robot = MoveRobot(
            base_speed=Literal(1),
            max_speed=Literal(1),
            movement=SumVectors(
            vectors=[ MoveTo(target=GlobalToEgocentric(
                             robot_pos=GetPosition(),
                                     global_pos=Literal( val=Vector( 49, 49 ) ) ) ),
                          AvoidObs(obs_list=GetObs(),
                                   safety_margin=Literal( val=1.5 ),
                                   sphere_of_influence=Literal( val=5 ) ),
                          Wander(persistence=Literal( val=10 ) ) ],
                weights=[ Literal( 1 ), Literal( 1 ), Literal( 0.3 ) ] ) )

################################################################################

    def connect_inputs( self ):
        pass

################################################################################

    def compute_output( self ):
        self.move_robot.get_output()
