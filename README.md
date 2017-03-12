# Artificial Intelligence Nanodegree

This project is from Udacity’s Artificial Intelligence Nanodegree program. It contains code from Udacity as well as my own.

## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: To solve the puzzle with the naked twins strategy we must limit our scope to sets of two-digit values per unit. If we encounter identical pairs in the same unit, we have found the naked twins and must proceed to remove both digits from their shared peers.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Simply adding the diagonal units at the beginning of the units list should be all there's needed to solve a diagonal sudoku, as long as it's solvable. The _only_choice_ function will process the diagonal units if included.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.


## Project Review

[Visit this page to see the final review](https://review.udacity.com/#!/reviews/346026/shared)