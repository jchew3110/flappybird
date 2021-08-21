# flappybird
This is my first git project!
Flappy Bird A.I. using NEAT and pygame

## Table of Contents
* [Technologies](#technologies)
* [Type of A.I.](#type-of-ai)
* [Things to consider for NEAT](#things-to-consider-for-neat)
* [Setup](#setup)

## Technologies
Project is created with:
* Python 3.9.0
* Pygame 2.0.1
* SDL 2.0.14
* NEAT 0.92

## Type of A.I.

NEAT (NeuroEvolution of Augmenting Topologies) is an evolutionary algorithm that creates artificial neural networks.
The main idea here is that NEAT starts simple. NEAT will change the weights of connections between input and output neurons and will randomly assign new nodes. It will also remove nodes and connections in favour of simpler topologies. 
Note this algorithm was developed in 2002 and thus runs on a CPU rather than GPU.
For more info -> http://nn.cs.utexas.edu/downloads/papers/stanley.cec02.pdf

## Things to consider for NEAT

### Inputs 
* Bird Y (position of the bird)
* Top Pipe (distance between bird and next top pipe)
* Bottom Pipe (distance between bird and next bottom pipe)

### Outputs 
* Jump 

### Activation Function
* TanH (hyperbolic tangent function so the value from the output neuron is -1 < x < 1) 

### Population Size
* 100 (The higher the population birds the more variance in each generation)
### Fitness Function
* Distance (A way of evaluating how good our birds are) 
### Max Generations
* 30
## Setup
To run this project download game.py, imgs and config-feedforward.txt then type in console:

```
$ python3 game.py

or 

$ python game.py

```
