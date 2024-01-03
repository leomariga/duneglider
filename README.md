# Dune Glider
A python model for a small glider.

## Newthon-Euler modeling
Just add a bunch of `Force` elements in your plane and run the simulation to see the 3D linear and angular states, such as position, velocity and acceleration.

## But I want to see and plot everything!
Add `Probe` to the signal you want to observe throughout the simulation and call `plot()` command. You can observe aircraft's states, forces or any numpy element you want.

## How to run
- Add your AVL path `duneglider/f_util/avl_config.cfg`
- Run `step.py`.