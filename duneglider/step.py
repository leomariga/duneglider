import numpy as np
from f_utils.axis import *
from glider_comp.plane import Plane
from glider_comp.force import Force


sim_seconds = 10
Ts = 0.1
p = Plane(Ts)

print(int(sim_seconds/Ts))

for dt in range(int(sim_seconds/Ts)):
    p.step()
    print(dt)

p.X_probe.plot()
p.Xp_probe.plot()
p.A_probe.plot()
p.force_sum.plot()