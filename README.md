# 3x3x3 Cube Puzzle Solver
![Package Installation](https://github.com/lopeLH/pypuzzle3d/workflows/Package%20Installation/badge.svg?branch=master)
![Tests](https://github.com/lopeLH/pypuzzle3d/workflows/Tests/badge.svg?branch=master)
![Python Linting](https://github.com/lopeLH/pypuzzle3d/workflows/Python%20Linting/badge.svg?branch=master)

While having a coffee at UCLouvain's caffeteria with some colleagues, I saw a 3x3x3 wooden cube sitting on a table. When out of curiosity I grabed it, it fell apart into 6 pieces. Scared for breaking it, I looked at one of my colleagues who said:

-- *"Don't worry. That puzzle is super easy to solve. In fact there are many different ways to assemble it."*

That made me wonder exactly how many different solutions that puzzle had... so I created this automatic, pseudo brute-force puzzle solver to figure out. 

This Python code is designed find all unique solutions of arbitrary 3x3x3 cube puzzles, exhaustively exploring the space of piece placement possitions, prunning the branches in which no solution can be found to make things faster. The solver takes the shape of the individual figures as the input.

Aside from standard libraries (numpy, matplotlib...), this code requires numba and seaborn libraries. 

Solutions are saved as images in the following format:

![alt text](https://github.com/lopeLH/3x3x3-Cube-Puzzle-Solver/blob/master/examples/solution-1.png)

