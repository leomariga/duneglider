import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from f_utils.axis import *

class Probe:

    def __init__(self, name, Ts, is_3D = True):
        self.name = name
        self.is_3D = is_3D
        self.value_array = []
        self.X_Array = []
        self.Y_Array = []
        self.Z_Array = []
        self.Ts = Ts

    def update(self, value):
        self.value_array.append(value)
        if self.is_3D:
            self.X_Array.append(value[0, 0])
            self.Y_Array.append(value[1, 0])
            self.Z_Array.append(value[2, 0])

    def plot(self):
        t_vector = np.arange(len(self.value_array))*self.Ts
        if self.is_3D:
            plt.plot(t_vector, np.array(self.X_Array), label=f"{self.name}_X")
            plt.plot(t_vector, np.array(self.Y_Array), label=f"{self.name}_Y")
            plt.plot(t_vector, np.array(self.Z_Array), label=f"{self.name}_Z")
        else:
            plt.plot(t_vector, np.array(self.value_array), label=f"{self.name}")
        plt.legend(loc="upper left")
        plt.show()