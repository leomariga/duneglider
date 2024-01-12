# Dune Glider
This repository contains an open-source development of a small glider model in python. The goal is to have fun with aerodynamic and physics related to aircraft optimization and modeling.

Dune Glider is small wing used in sandboard. The goal is to create lift during a descent slope and glide during a slow drop from a dune. The goal is not to have a super high lift such as hang gliders, but a small, fun (and mostly safe) drop. This concept can also be applied snowboard. Some people is already trying concepts like this using REEDIN SUPERWING models, but this is not exactly optimizd for this purposes. 

## Newthon-Euler modeling
Just add a bunch of `Force` elements in your plane and run the simulation to see the 3D linear and angular states, such as position, velocity and acceleration.

## But I want to see and plot everything!
Add `Probe` to the signal you want to observe throughout the simulation and call `plot()` command. You can observe aircraft's states, forces or any numpy element you want.

## How to run
- Add your AVL path `duneglider/f_util/avl_config.cfg`
- Run `step.py`.