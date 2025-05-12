# Boids Simulation
An academic project to demonstrate understanding of **Formal Languages**, **Finite Automata**, and **Computability Theory** through a Boids (Bird-oid objects) simulation.

**Contributors:** Carter Close, James DeZurik

## Overview
Boids is an artificial life simulation created to model bird flocking patterns. Originally created by Craig Reynolds, the main algorithm is determined by three unique principles:
- **Separation** - Boids will maintain a minimum distance from each other to avoid overflocking.
- **Alignment** - Boids adjust their velocity to align with others in the flock.
- **Cohesion** - Boids will move towards the center of mass of the flock.

This project aims to extend the basic algorithm by introducing fatigue modeling using a finite state machine. This simulates accurate energy levels and slipstreaming within boid flocks.

## Fatigue Model
To simulate fatigue, we implemented a state-based fatigue system into the algorithm:
- Boids **lose energy** when flying alone or leading a flock.
- Boids **regain energy** when flying with others or in the middle of a flock, simulating the slipstream effect.
- Fatigue affects speed:
    - **More fatigued** boids will slow down.
    - **Less fatigued** boids will maintain their speed.
- Visualized with a color gradient:
    - **White -> Yellow -> Red** to represent increasing levels of fatigue.

This approach provides an approximate representation of the aerodynamical properties and processes of real bird flocks, where lead birds tire and are eventually overtaken by other birds.

## Running the Simulation
This simulation is exclusively visual, there are no interactive pieces. While originally considered, it was ultimately out of scope for this version of the project.

### Requirements
- Any recent version of Python 3.
- No additional dependencies required.

### Steps to Run
1. Clone this repository:
  ```
  git clone https://github.com/JamDeZurik/FiniteBoids.git
  ```
2. Navigate to the project directory and run the script:
  ```
  cd FiniteBoids
  python Main.py
  ```

## Acknowledgements
We acknowledge that this simulation and model are not, and ultimately cannot be, perfectly accurate to represent real bird flocking and biological patterns. 
Instead, this model aims to provide an exploration into the question: 
> **"How would flocking behavior look if fatigue was modeled with a state machine?"**

There are multiple opportunities for future improvements in simulation quality and realism to be made.
