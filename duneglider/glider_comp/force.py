
from dataclasses import dataclass, field
from f_utils.axis import *

@dataclass
class Force:
    """
    A class to store properties of force applyed to an object.

    Args:
        N: Force vector
        P: Position of applyed for respective to the center of mass (used to calculate the moment)
        frame: frame which this force is aplied, can be `body` or `inertial`

    """
    N: Array3x1 = field(default_factory=lambda: nat([0, 0, 0])) 
    P: Array3x1 = field(default_factory=lambda: nat([0, 0, 0])) 
    frame: str  = 'body'
    name: str   = ''

    # def __str__(self) -> str:
    #     return f'Vector: {self.N}, Pos: {self.P}, Frame {self.frame}'
    
    def __repr__(self) -> str:
        return f'Vector {self.name}: {self.N.T}, Pos: {self.P.T}, Frame {self.frame}'