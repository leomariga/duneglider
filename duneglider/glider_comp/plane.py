import numpy as np
from f_utils.axis import *
from glider_comp.force import Force


class Plane:
    """
    Data with plane properties.

    Args:
        X:  Position in a 3D environment
        Xp: Velocity in a 3D environment
        A:  Attitude in a 3D environment
        Ap: Angular velocity in a 3D environment
    """

    X:  Array3x1 = nat([0, 0, 0]) # inertial
    V: Array3x1 = nat([0, 0, 0])  # body

    A:  Array3x1 = nat([0, 0, 0]) # inertial
    w: Array3x1 = nat([0, 0, 0]) # body

    force_list: list[Force] = []

    clw: float = 1
    cdw: float = 0.4
    S:   float = 3.3
    ro:  float = 1.225
    m:   float = 20
    g:   float = 9.8
    I = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    def __init__(self):
        pass

    def get_wing_lift(self):
        L = -(self.clw*self.ro*self.get_CAS()**2*self.S)/2
        return Force(N=nat([0, 0, L]), name='Wing lift')
    
    def get_wing_induced_drag(self):
        D = -(self.cdw*self.ro*self.get_CAS()**2*self.S)/2
        return Force(N=nat([0, D, 0]), name='Wing induced drag')
    
    def get_weight(self):
        Wi = self.m*self.g
        Wi_np = nat([0, 0, Wi])
        Wb = Ritb(Wi_np, self.A)
        return Force(N=Wb, name='Weight')

    def add_force(self, f: Force):
        self.force_list.append(f)

    def get_CAS(self):
        return self.V[0, 0]
    
    def step(self, Ts):
        self.add_force(self.get_wing_lift())
        self.add_force(self.get_wing_induced_drag())
        self.add_force(self.get_weight())

        sum_forces = nat([0, 0, 0])
        sum_moments = nat([0, 0, 0])
        for f_i in self.force_list:
            sum_forces = sum_forces + f_i.N
            sum_moments = sum_moments + np.cross(f_i.P, f_i.N, axis=0) 
        
        # Newthon euler motion model
        # We assume the CG is in the [0, 0, 0] from coordinate axis
        print(sum_forces)
        print(sum_moments)

        # Mass and inertia matrix component (spatial inertia)
        Z3x3 = np.zeros((3,3))
        mI3x3 = np.eye(3)*self.m
        MII = np.asarray(np.bmat([[mI3x3, Z3x3], [Z3x3, self.I]]))

        # Force and moment component
        MFT = np.asarray(np.bmat([[sum_forces], [sum_moments]]))

        # Fictious force component
        MFFup = np.cross(self.w, self.m*self.V, axis=0)
        MFFdown = np.cross(self.w, self.I @ self.w, axis=0)
        MFF = np.asarray(np.bmat([[MFFup], [MFFdown]]))

        # Calculate state transition matrix
        # Done!
        MA = np.linalg.inv(MII) @ (MFT - MFF)
        print(MA)

