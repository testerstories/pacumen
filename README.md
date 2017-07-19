## Pacumen

The name of this project is based on the name "Pac-Man" and the word "acumen." The term generally refers to the ability to make good judgments and quick decisions. This is often done in a particular domain.

To that end, **Pacumen** is an implementation of the [Pacman AI project](http://ai.berkeley.edu) developed at UC Berkeley. This is a project that allows you to provide customized Pac-Man variations and then apply learning algorithms to those variations. I'm using this project as part of my studies into reinforcement learning as well as a means by which to get software test specialists up to speed on how to consider quality when testing in such a context.

In terms of the Berkeley AI code, it's a bit of a nightmare of poor coding in many ways. My plan is to modify a lot of the existing code to make it more in line with good Python coding practices as well as make it more modular and thus easier to maintain. I've also had to fix a few bugs they had in their code.

One of my original plans was to update the code to run on Python 3. **Currently Pacumen requires the Python 2.x branch.** The main complication for conversion is the heavy usage of Tkinter. The benefit of this has been not having to use external graphics libraries. The downside is that the changes with Tkinter between Python 2 and 3 are annoying to work with when you just want to get something done.

### Layouts

A core concept in this repository is that of a layout, which serves as a representation of a Pac-Man game board. One thing that's interesting about the grids that make up the Pac-Man board is that the origin point (0,0) is considered to be the _bottom left_ of the grid, and not the _top left_. The `y` coordinate is considered the height of the grid while the `x` coordinate is the width of the grid.

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
