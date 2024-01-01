import numpy as np
from f_utils.axis import *
from glider_comp.force import Force
from glider_comp.probe import Probe


class Plane:
    """
    Data with plane properties.

    Args:
        X:  Position in a 3D environment (inertial frame)
        Xp: Linear velocity in a 3D environment (inertial frame)
        V:  Linear velocity in a 3D environment (body frame)
        Vp: Linear aceleration in a 3D environment (body frame)

        A:  Attitude in a 3D environment (inertial frame)
        Ap: Angular velocity in a 3D environment (inertial frame)
        w:  Angular velocity in a 3D environment (body frame)
        wp: Angular aceleration in a 3D environment (body frame)
    """

    X:  Array3x1 = nat([0, 0, 0])  # inertial
    Xp: Array3x1 = nat([0, 0, 0])  # inertial
    V:  Array3x1 = nat([0, 0, 0])  # body
    Vp: Array3x1 = nat([0, 0, 0])  # body

    A:  Array3x1 = nat([0, 0, 0]) # inertial
    Ap: Array3x1 = nat([0, 0, 0]) # inertial
    w:  Array3x1 = nat([0, 0, 0]) # body
    wp: Array3x1 = nat([0, 0, 0]) # body

    force_list: list[Force] = []
    probe_list: list[Probe] = []

    clw: float = 1
    cdw: float = 0.4
    S:   float = 3.3
    ro:  float = 1.225
    m:   float = 20
    g:   float = 9.8
    I = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])




    def __init__(self, Ts):
        # Add probes for simulation
        self.X_probe = Probe('Position', Ts)
        self.Xp_probe = Probe('Linear velocity (I)', Ts)
        self.V_probe = Probe('Linear velocity (B)', Ts)
        self.Vp_probe = Probe('Linear aceleration (B)', Ts)
        self.A_probe = Probe('Angular position', Ts)
        self.Ap_probe = Probe('Angular velocity (I)', Ts)
        self.w_probe = Probe('Angular velocity (B)', Ts)
        self.wp_probe = Probe('Angular acceleration (B)', Ts)

        self.force_lift = Probe('Lift (I)', Ts)
        self.force_drag = Probe('Drag (I)', Ts)
        self.force_weight = Probe('Weight (I)', Ts)
        self.force_thrust = Probe('Thrust (I)', Ts)

        self.force_sum = Probe('Force (I)', Ts)

        self.Ts = Ts


    def get_wing_lift(self):
        L = -(self.clw*self.ro*self.get_CAS()**2*self.S)/2
        return Force(N=nat([0, 0, L]), name='Wing lift')
    
    def get_wing_induced_drag(self):
        D = -(self.cdw*self.ro*self.get_CAS()**2*self.S)/2
        return Force(N=nat([D, 0, 0]), name='Wing induced drag')
    
    def get_weight(self):
        Wi = self.m*self.g
        Wi_np = nat([0, 0, Wi])
        Wb = Ritb(Wi_np, self.A)
        return Force(N=Wb, name='Weight')
    
    def get_thrust(self):
        return Force(N=nat([20, 0, 0]), name='Thrust')
    
    def add_force(self, f: Force):
        self.force_list.append(f)

    def get_CAS(self):
        return self.V[0, 0]
    
    def step(self):
        self.force_list = []

        F_L = self.get_wing_lift()
        self.add_force(F_L)
        self.force_lift.update(Rbti(F_L.N, self.A))

        F_Di = self.get_wing_induced_drag()
        self.add_force(F_Di)
        self.force_drag.update(Rbti(F_Di.N, self.A))

        F_w = self.get_weight()
        self.add_force(F_w)
        self.force_weight.update(Rbti(F_w.N, self.A))

        F_T = self.get_thrust()
        self.add_force(F_T) # TEST
        self.force_thrust.update(Rbti(F_T.N, self.A))

        # Add probe to observe force in inertial frame

        sum_forces = nat([0, 0, 0])
        sum_moments = nat([0, 0, 0])
        for f_i in self.force_list:
            sum_forces = sum_forces + f_i.N
            sum_moments = sum_moments + np.cross(f_i.P, f_i.N, axis=0) 

        self.force_sum.update(Rbti(sum_forces, self.A))
        
        # Newthon euler motion model
        # We assume the CG is in the [0, 0, 0] from coordinate axis

        # Mass and inertia matrix component (spatial inertia)
        Z3x3 = np.zeros((3,3))
        mI3x3 = np.eye(3)*self.m
        MII = np.asarray(np.bmat([[mI3x3, Z3x3], [Z3x3, self.I]]))

        # Force and moment component
        MFT = np.asarray(np.bmat([[sum_forces], [sum_moments]]))

        # Fictitious force component
        MFFup = np.cross(self.w, self.m*self.V, axis=0)
        MFFdown = np.cross(self.w, self.I @ self.w, axis=0)
        MFF = np.asarray(np.bmat([[MFFup], [MFFdown]]))

        # Calculate state transition matrix
        # Done!
        MA = np.linalg.inv(MII) @ (MFT - MFF)

        # Acceleration vectors in a discrete environment (body frame)
        self.Vp = np.asarray([MA[0:3, 0]]).T
        self.wp = np.asarray([MA[3:, 0]]).T

        # Velocity vector in a discrete environment (body frame)
        self.V = self.V + self.Vp*self.Ts
        self.w = self.w + self.wp*self.Ts

        # Velocity vector in a discrete environment (inertial frame)
        self.Xp = Rbti(self.V, self.A)
        self.Ap = Tbti(self.w, self.A)

        # Position vector in a discrete environment (inertial frame)
        self.X = self.X + self.Xp*self.Ts
        self.A = self.A + self.Ap*self.Ts

        self.X_probe.update(self.X) 
        self.Xp_probe.update(self.Xp)
        self.V_probe.update(self.V) 
        self.Vp_probe.update(self.Vp)
        self.A_probe.update(self.A) 
        self.Ap_probe.update(self.Ap)
        self.w_probe.update(self.w) 
        self.wp_probe.update(self.wp)



