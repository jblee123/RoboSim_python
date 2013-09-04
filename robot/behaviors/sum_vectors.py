from behavior_imports import *

SumVectorsError = 'SumVectorsError'

################################################################################

class SumVectors(Behavior):
    def __init__( self, name=None, vectors=None, weights=None ):
        Behavior.__init__( self, name )
        self.vectors = vectors
        self.weights = weights

################################################################################

    def compute_output( self ):
        if ( self.vectors == None ):
            raise SumVectorsError, 'vectors input not set'

        if ( self.weights == None ):
            raise SumVectorsError, 'weights input not set'

        if ( len( self.vectors ) != len( self.weights ) ):
            raise SumVectorsError, 'len( vectors ) != len( weights )'

        self.output = Vector( 0, 0, 0 )

        i = 0
        while ( i < len( self.vectors ) ):
            vec = self.vectors[i].get_output() * self.weights[i].get_output()
            self.output = self.output + vec
            i = i + 1

################################################################################

if __name__ == '__main__':
    print 'SumVectors'

    vec1 = Literal( Vector(0,1) )
    vec2 = Literal( Vector(1,0) )

    coop = SumVectors()
    coop.setVal( 'vectors', [vec1, vec2] )
    coop.setVal( 'weights', [ Literal(2), Literal(3) ] )

    print 'coop.get_output() =', coop.get_output()

