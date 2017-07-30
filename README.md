## Pacumen

![pacumen](http://testerstories.com/files/pacumen/pacman.png)

The name of this project is based on the name "Pac-Man" and the word "acumen." The term generally refers to the ability to make good judgments and quick decisions. This is often done in a particular domain.

To that end, **Pacumen** is an implementation of the [Pacman AI project](http://ai.berkeley.edu) developed at UC Berkeley. This is a project that allows you to provide customized Pac-Man variations and then apply learning algorithms to those variations. I'm using this project as part of my studies into reinforcement learning as well as a means by which to get software test specialists up to speed on how to consider quality when testing in such a context.

In terms of the Berkeley AI code, it's a bit of a nightmare of poor coding in many ways. My plan is to modify a lot of the existing code to make it more in line with good Python coding practices as well as make it more modular and thus easier to maintain. I've also had to fix a few bugs they had in their code. I have also modified the code to run under Python 2.x and Python 3.x. The complicated parts here were making sure TKinter could work on both.

### Goal

The goal of the project is to use Pac-Man as a problem-solving environment for experiments about general artificial intelligence and learning algorithms.

This is an environment that can easily map onto the general definitions of search problems and decision processes. These are what characterize most approaches to artificial intelligence.

Pac-Man consists of objects moving around on a set of squares that can be modeled as a grid. At any given time Pac-Man occupies a square and faces one of the four directions: north, south, east, or west. There may be walls in between the square or entire squares might be blocked by walls. Regardless, the location of Pac-Man is determined by the x and y coordinates of the grid as such:

![pacumen-grid](http://testerstories.com/files/pacumen/pacumen-grid.png)

### Usage

`Pacumen` provides a very basic Pac-Man game. In the game, you control the movements of Pac-Man using arrow keys on your keyboard. You can also use the traditional gamer WASD keys: w (up), s (down), a (left), d (right).

Go ahead and try it.

```
python pacman.py
```

The goal of the project is write agent programs to control the actions of Pac-Man. That is, creating a Pac-Man agent. The project enables you to use different environments to try out your Pac-Man agent programs. For example, try these:

```
python pacman.py --layout test_maze
```

```
python pacman.py --layout tiny_maze
```

You can also vary the scale of the screen by using the "zoom" option as shown below:

```
python pacman.py --layout tiny_maze --zoom 2
```

```
python pacman.py --layout big_maze --zoom 0.5
```

More instructions about how to utilize the Pacumen context for algorithms will be coming soon.

### Searching Algorithms

Before an agent can begin to make decisions, it needs to find the best/correct answer to the question/problem it's trying to solve. The first part is done with search algorithms. The problems are presented in the form of a game board.

You must implement generic search algorithms that will be called by pacman agents. These algorithms will go in the `search.py` file. In that file, there are methods put in place for you as placeholders:

* depth_first_search()
* breadth_first_search()
* uniform_cost_search()
* astar_search()

Aliases for these are dfs(), bfs(), ucs(), and astar().

These algorithms will be passed in as the search function to be used by the search agent.

You can create your own search agents but the basis of one is already in place for you. This is called `SearchAgent` and is in the `agents_search.py` file. This is a very general search agent that finds a path through the maze. It does so using a **supplied search algorithm** for a **supplied search problem** and using a **supplied heuristic**.

By default, a SearchAgent tries to run a "depth first search" on a "position search problem" and uses a "null heuristic".

A **heuristic function** estimates the cost from the current state to the nearest goal in the provided SearchProblem. A null heuristic always returns a value of 0, which is a trivial heuristic stating that there is no cost.

#### SearchAgents are Agents

To see how this works, understand that a SearchAgent is a specific kind of generic `Agent`.

* Any agent must define a `get_action()` method. This method receives a GameState and must return a direction constant, such as Direction.NORTH or Direction.WEST.

* Further, an agent can define a `register_initial_state()` method and that will be called if it exists. This method is used to inspect the starting state.

Let's consider how these work in a basic SearchAgent.

* The register_initial_state() method is called and this is the first time that the agent sees the layout of the game board. In SearchAgent, this method chooses a path to the goal. In this phase, the agent should compute the path to the goal and store this information. An actions variable is used to store the path (which is found by calling the search algorithm/function on the search problem). A total_cost variable stores the total cost of all those actions.

* The get_action() method returns the next action in the path chosen in register_initial_state(). The method will return Direction.STOP if there is no further action to take.

#### PositionSearchProblems are SearchProblems

A `PositionSearchProblem` (which is a specific kind of generic `SearchProblem`) can be used to find paths to a point on the pacman board. By default, this problem has been fully specified and finds location (1, 1). A generic SearchProblem outlines the structure of a search problem. Specifically, a search problem defines the state space, start state, goal test, successor function and cost function. Keep in mind that the state space consists of (x, y) positions in a pacman game.

Any search problem must provide the following elements:

* A `get_start_state()` method, which returns the start state for the search problem.

* An `is_goal_state()` method is also required. This method should return True if and only if the state is a valid goal state.

* A `get_successors()` method is required. For a given state, this method should return a list of triples: successor, action, and step cost. Here 'successor' is a successor to the current state, 'action' is the action required to get to that successor state, and 'step cost' is the incremental cost of expanding to that successor.

* A `get_cost_of_actions()` method must be provided. This method returns the total cost of a sequence of actions. The sequence must be composed of legal moves.

Let's consider how these work in the context of PositionSearchProblem.

* The get_start_start() method will simply return the starting state, which is basically the position where the pacman agent starts, as determined by the layout.

* The is_goal_state() method checks if the current state matches the goal state. The goal state is defined by the problem and for PositionSearchProblem the default goal state is (1,1).

* The get_successors() method returns successor states, the actions they require, and a cost that is defined by the problem. For PositionSearchProblem, the cost function is by default 1.

* The get_cost_of_actions() method returns the cost of a particular sequence of actions, simply by incrementing the cost based on the cost function. So, in this case, every action has a cost of 1. If the sequence of actions includes an illegal move, this method returns 999999.

#### Execution of Search Problems

You can run the generic search agent like this:

    python pacman.py --layout tiny_maze --pacman SearchAgent

However, unless you have created a depth first search function, which is the default, you will see something like this:

    [SearchAgent] using function depth_first_search
    [SearchAgent] using problem type PositionSearchProblem
    *** Method not implemented: depth_first_search

The above command is identical to doing this:

    python pacman.py --layout tiny_maze --pacman SearchAgent -a fn=dfs

Here I’m just passing in the name of the search function, in this case "dfs". I could have also said "depth_first_search". Whatever you type here must be a function that you have provided.

### Moving Parts

Everything in this section is likely to be modified or consolidated at some point in the future. It's all accurate, but not presented in the best format.

#### Agents

There is an `Agent` class that is very basic but defines the mode of operation, which is that agents will be executing in the context of the game. Pac-Man is an agent. So are the ghosts. Note that in classic Pac-Man, Pac-Man is always agent 0. The ghosts are then given numbers from 1 up.

An agent instance must define a `get_action` method, which essentially dictates how the agent moves about in the game world. An agent instance may also define a `register_initial_state` method, which does what it sounds like: sets up an initial state for the agent, such as a particular position.

All agents will receive a `GameState` and must return an action it is of type `Direction`.

There is also the concept of an `AgentState`. These instances hold just what it sounds like: the state of an agent. This state includes aspects like configuration, speed, "scared" (in the case of ghosts), and so on.

#### Actions

There is an `Actions` class and it serves as a collection of static methods for manipulating move actions in the game world.

#### Rules

There is a `GameRules` class that serve as basic rules for managing the control flow of a game, deciding when and how the game starts and ends. A specific set of rules, in the `PacmanRules` class specifically govern how the pacman agent interacts with the environment under the basic game rules. Likewise, `GhostRules` dictates how ghosts interact with the environment.

Collectively these classes are in place to make sure that the game world has rules and that any relevant agents -- Pac-Man and the ghosts -- follow those rules.

### Configuration

A `Configuration` instance holds the (x,y) coordinate of an agent, along with its traveling direction. The convention for positions, like a graph, is that (0,0) is the lower left corner, x increases horizontally and y increases vertically. This means north is the direction of increasing y, or (0,1).

An important method here is `generate_successor()` which generates a new configuration reached by translating the current configuration by the action vector. This is a low-level call and does not attempt to respect the legality of the movement. It should be noted that actions are movement vectors.

#### Game Control

Three main classes are `Game`, `GameState` and `GameStateData`. A The Game instance manages the control flow, soliciting actions from agents.

The `run()` method for the game instance is the main control loop for game play. In this method, `self.state` is a GameState instance while `self.state.data` is a GameStateData instance.

The idea of `GameStateData` is that it generates a new data state from a layout array. If there is a previous state, the new state is generated by copying information from the predecessor state. This state data is wrapped up in the GameState.

The idea of the `GameState` is that it generates a new game state from game state data and thus from a layout array. If there is a previous state, the new state is generated by copying information from its predecessor.

It's important to understand that a GameState specifies the full game state, including the food ("pac dots"), capsules ("power pellets"), agent configurations and score changes. GameStates are used by the Game object to capture the actual state of the game and can be used by agents to reason about the game. Much of the information in a GameState is stored in a GameStateData object. The GameState provides accessor methods for getting to this data, as opposed to referring to the GameStateData object directly.

There are many accessor methods to be aware of.

##### Game State Accessors

* get_and_reset_explored: You can reset the part of the game world that has been explored by Pac-Man. 

* get_legal_actions: Returns the legal actions for the agent specified.

* get_legal_pacman_actions: Returns the legal actions for the pacman agent.

* generate_successor: Returns the successor state after the specified agent takes the action.

* generate_pacman_successor: Generates the successor state after the specified pacman move.

* get_pacman_state: Returns an AgentState object for the pacman agent. This includes information like the position and the direction Pac-Man is facing.

* get_pacman_position: Returns the position of Pac-Man, which is one aspect of his state.

* get_ghost_states:
* get_ghost_state: Returns the AgentState object for a given ghost agent. This includes information like the position of the ghost and its direction of motion.

* get_ghost_position: Returns the position of a specific ghost agent, which is one aspect of its state.

* get_ghost_positions: Returns the positions of all ghost agents in teh game world.

* get_num_agents: Returns the number of agents that are present in the world.

* get_score: Returns the current score of the game.

* get_capsules: Returns a list of positions (x,y) of the remaining capsules, which are the power pellets.

* get_num_food: Returns a count of the food ("pac dots") that still exist in the game world; meaning food that Pac-Man has not eaten.

* get_food: Returns a Grid of boolean food indicator variables. Grids can be accessed via list notation, so to check if there is food at (x,y), just do this:

```
current_food = state.get_food()
if current_food[x][y] == True: ...
```

get_walls: Returns a Grid of boolean wall indicator variables. Grids can be accessed via list notation, so to check if there is a wall at (x,y), just do this:

```
walls = state.getWalls()
if walls[x][y] == True: ...
```

* has_food: Checks if a given location has food.

* has_wall: Checks if a given location is a wall.

* is_lose: Checks if a move is a losing move, which would be the case of Pac-Man getting eaten.

* is_win: Checks if a move is a winning move, which in most circumstances will be Pac-Man eating all of the food on a grid.

#### Grid

A Grid instance represents a two-dimensional array of objects backed by a list of lists. Data is accessed via `grid[x][y]` where (x,y) are positions on a Pac-Man map with x horizontal, y vertical and, most importantly, the origin (0,0) in the bottom left corner. The `__str__` method of this class constructs an output that is oriented like a pacman board.

There is a `pack_bits()` method that returns an efficient int list representation. There is also an `unpack_bits()` method that fills in data from a bit-level representation.


#### Layouts

A core concept in this repository is that of a layout, which serves as a representation of a Pac-Man game board.

A `Layout` instance manages the static information about the game board. The layout text provides the overall shape of the maze. Each character in the text represents a different type of object.

* P - Pacman
* G - Ghost
* . - Food Dot
* o - Power Pellet
* % - Wall

Any other characters are ignored.

One of the core methods is `process_layout_text()`. This method modifies coordinates from the input format to a more standard (x,y) convention.

Also important is the `process_layout_character()` method. For each individual character in a layout board, this method will update an appropriate data structure (agent_positions, walls, food, capsules) to reflect the presence of that character.

One thing that's interesting about the grids that make up the Pac-Man board is that the origin point (0,0) is considered to be the _bottom left_ of the grid, and not the _top left_. The `y` coordinate is considered the height of the grid while the `x` coordinate is the width of the grid.

#### Test Maze

Consider this `test_maze` layout:

    %%%%%%%%%%
    %.      P%
    %%%%%%%%%%

Here the `%` character represents a wall, the `.` represents a food dot (called "Pac Dots" in the game), and `P` indicates the Pac-Man character.

Here is how _Pacumen_ represents this:

    layout.height: 3
    layout.width: 10

    Walls:
    TTTTTTTTTT
    TFFFFFFFFT
    TTTTTTTTTT

    Dots:
    FFFFFFFFFF
    FTFFFFFFFF
    FFFFFFFFFF

    Pellets:
    []

    Agents:
    [(True, (8, 1))]

For the walls, notice how the `F` portions correspond only to those parts that are _not_ walls. For the dots, notice how the lone `T` is indicating that a food dot was found in only one spot in this representation. There are no power pellets in this maze so no location is recorded for them.

Incidentally, the above representation is generated internally by this kind of list of (y,x) coordinates:

    [2][0] [2][1] [2][2] [2][3] [2][4] [2][5] [2][6] [2][7] [2][8] [2][9]
      %      %      %      %      %      %      %      %      %      %

    [1][0] [1][1] [1][2] [1][3] [1][4] [1][5] [1][6] [1][7] [1][8] [1][9]
      %       .                                               P      %

    [0][0] [0][1] [0][2] [0][3] [0][4] [0][5] [0][6] [0][7] [0][8] [0][9]
      %      %      %      %      %      %      %      %      %      %

Entities like Pac-Man are treated as _agents_. The above shows that Pac-Man was found at an x position of 8 and a y position of 1.

#### Test Modified

Here's a modified maze, which is a variation on the `test_classic` maze:

    %%%%%
    % o %
    %.G.%
    % . %
    %. o%
    %   %
    %  .%
    %   %
    %P .%
    %%%%%

Here we have the addition of a ghost agent (represented by `G`) and two power pellets, represented by `o`. (Power pellets are things Pac-Man can eat which allow him to eat the ghosts.) Here is how _Pacumen_ represents this:

    layout.height: 10
    layout.width: 5

    Walls:
    TTTTT
    TFFFT
    TFFFT
    TFFFT
    TFFFT
    TFFFT
    TFFFT
    TFFFT
    TFFFT
    TTTTT
    
    Dots:
    FFFFF
    FFFFF
    FTFTF
    FFTFF
    FTFFF
    FFFFF
    FFFTF
    FFFFF
    FFFTF
    FFFFF

    Pellets:
    [(3, 5), (2, 8)]

    Agents:
    [(True, (1, 1)), (False, (2, 7))]

Here you can see the pellets and the ghost are both represented. Given that this board is a bit larger, you can see how the coordinates for the pellets and the agents are starting from the bottom left.

Regarding the "True" and "False" for the agents, these are simply used to indicate the "agent of concern" or "agent of control." In this case, Pac-Man is the agent that we are concerned with applying machine learning to and is the one that we want to control. The other agent does not fit into that category.
