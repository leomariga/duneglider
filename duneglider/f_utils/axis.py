import numpy as np
from typing import Annotated, Literal, TypeVar
import numpy.typing as npt

# A list of most used types
DType = TypeVar("DType", bound=np.generic)

Array3x1 = Annotated[npt.NDArray[DType], Literal[3, 1]]

"""
Smaller way to create numpy row arrays from lists

Args:
    l: List or list of lists to be transformed in numpy array

Returns:
    nparray_l: row array for l
"""
def na(narray):
    if not isinstance(narray[0], list):
        narray = [narray]
    return np.array(narray)


"""
Smaller way to create numpy column arrays from lists

Args:
    l: List or list of lists to be transformed in numpy array

Returns:
    nparray_l: Column array for l
"""
def nat(narray) -> Array3x1:
    if not isinstance(narray[0], list):
        narray = [narray]
    return np.array(narray).T



"""
Rotation matrix body to intertial

Args:
    Xb: Column array for point in body axis
    A: Column array for attitude

Returns:
    Xi: Column array for P in intertial axis
"""
def Rbti(Xb, A):

    phi   = A[0, 0]
    theta = A[1, 0]
    psi   = A[2, 0]

    Rbti = np.array([[np.cos(theta)*np.cos(psi), np.sin(phi)*np.sin(theta)*np.cos(psi)-np.cos(phi)*np.sin(psi),  np.cos(phi)*np.sin(theta)*np.cos(psi)+np.sin(phi)*np.sin(psi)],
                     [np.cos(theta)*np.sin(psi), np.sin(phi)*np.sin(theta)*np.sin(psi)+np.cos(phi)*np.cos(psi),  np.cos(phi)*np.sin(theta)*np.sin(psi)-np.sin(phi)*np.cos(psi)],
                     [-np.sin(theta),            np.sin(phi)*np.cos(theta),                                      np.cos(phi)*np.cos(theta)                                    ]])
    

    Xi = Rbti @ Xb

    return Xi



"""
Rotation matrix inertial to body

Args:
    Xi: Column array for point in body axis
    A: Column array for attitude

Returns:
    Xb: Column array for P in intertial axis
"""
def Ritb(Xi, A):
    
    phi   = A[0, 0]
    theta = A[1, 0]
    psi   = A[2, 0]

    Rbti = np.array([[np.cos(theta)*np.cos(psi), np.sin(phi)*np.sin(theta)*np.cos(psi)-np.cos(phi)*np.sin(psi),  np.cos(phi)*np.sin(theta)*np.cos(psi)+np.sin(phi)*np.sin(psi)],
                     [np.cos(theta)*np.sin(psi), np.sin(phi)*np.sin(theta)*np.sin(psi)+np.cos(phi)*np.cos(psi),  np.cos(phi)*np.sin(theta)*np.sin(psi)-np.sin(phi)*np.cos(psi)],
                     [-np.sin(theta),            np.sin(phi)*np.cos(theta),                                      np.cos(phi)*np.cos(theta)                                    ]])
    

    Xb = Rbti.T @ Xi

    return Xb


"""
Angular velocity Rotation matrix body to intertial

Args:
    Apb: Column array for current angular velocity in body reference frame
    A: Column array for attitude

Returns:
    Api: Column array for Ap in intertial axis
"""
def Rvbti(Apb, A):

    phi   = A[0, 0]
    theta = A[1, 0]
    psi   = A[2, 0]

    Ritb = np.array([[1, 0, -np.sin(theta)],
                     [0, np.cos(phi), np.cos(theta)*np.sin(phi)],
                     [0, -np.sin(phi), np.cos(phi)*np.cos(theta)]])
    
    Rbti =  np.linalg.inv(Ritb)
    Api = Rbti @ Apb

    return Api

"""
Angular velocity Rotation matrix inertial to body

Args:
    Api: Column array for current angular velocity in inertial reference frame
    A: Column array for attitude

Returns:
    Apb: Column array for Ap in body axis
"""
def Rvbti(Apb, A):

    phi   = A[0, 0]
    theta = A[1, 0]
    psi   = A[2, 0]

    Ritb = np.array([[1, 0, -np.sin(theta)],
                     [0, np.cos(phi), np.cos(theta)*np.sin(phi)],
                     [0, -np.sin(phi), np.cos(phi)*np.cos(theta)]])
    
    Apb = Ritb @ Apb

    return Apb