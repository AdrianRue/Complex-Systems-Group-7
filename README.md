# Cellular Automata Star Formation Simulation(group 7)

![Animation](https://github.com/AdrianRue/Complex-Systems-Group-7/blob/main/Resultdisplay.GIF "Star Formation")

## Core Objective
The main goal of this project is to investigate the effect of initial conditions on star formation within a cellular automaton (CA) model. By altering the initial mass and spatial distributions, we aim to understand the parameters that significantly influence the emergence of stars in our simulated universe.

## Research Question
The primary research question addresses the impact of spatial distribution on star formation within a CA framework:
> Investigation into how the initial conditions affects star formation within a cellular automaton (CA) model 

> What is the effect of the spatial distribution of initial conditions on a cellular automata star formation model?


## Hypothesis
Our null hypothesis (H0) states:
> Variations in initial mass distributions in the simulated space will significantly influence star formation.


## Getting Started
To run this simulation, you will need Python and the following dependencies installed:
```
pip install -r requirements.txt
```

### Testing
To test the functionalities run:
```
pytest
```

### File Descriptions
`Agent.py`: Defines the Agent class, which represents astrophysical entities in the simulation.

`CellularAutomaton.py`: Contains the CellularAutomaton class that models the cellular space and rules for star formation.

`Group.py`: Contains the Group class for managing collections of agents.

`main.py`: The main script for initializing and running the simulation.

### Usage
```
usage: main.py [-h] [--one ONE] [--N N] [--prob_gas PROB_GAS] [--proto_size PROTO_SIZE] [--star_size STAR_SIZE] [--steps_dissipating STEPS_DISSIPATING]

options:
  -h, --help            show this help message and exit
  --one ONE             Run one sim or run all sims (default: True)
  --N N                 Grid size (default: 100)
  --prob_gas PROB_GAS   Probability of cell being a gas particle (default: 0.1)
  --proto_size PROTO_SIZE
                        Size needed to form proto star (default: 20)
  --star_size STAR_SIZE
                        Size needed to form star (default: 100)
  --steps_dissipating STEPS_DISSIPATING
                        Steps dissipation (default: 50)
```


### Results
the results of the simulation are depicted in the `Resultdisplay.GIF` file and `results`directory, illustrating the progression of star formation in the CA grid.


A few essential functions have tests in the `tests`directory

## Prerequisites
A `requirements.txt` file has been provided, this should install any necessary libraries





























