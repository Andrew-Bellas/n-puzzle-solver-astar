# n-puzzle-solver-astar
A solver for n-puzzles using A*

The first assignment in COMP-SCI 441 (Introduction to Artifical Intelligence) as well as my first experience with Python

## Usage

`python n-puzzle-astar.py [OPTIONS]`

### Options

|     OPTION    |                      Description                 |
| ------------- | ------------------------------------------------ | 
| --nvalue, -n  |  the puzzle size (3, 8, 15 etc), defaults to 8.  |
| --file, -f    |  specify the input file, defaults to input.txt   |

### Input

The input file must be a `.txt` file in the following format:

* First line: An integer representing the number of puzzles in the file
* All remaining lines: Rows containing space-seperated values with an empty row seperating boards

An example input file can be found [here](https://github.com/Andrew-Bellas/n-puzzle-solver-astar/blob/main/input.txt)

### Examples

Solve the 8 puzzle(s) located in `input.txt` 

```
python n-puzzle-astar
```

Solve the 15 puzzle(s) located in `my_puzzlols.txt`

```
python n-puzzle-astar -f my_puzzlols.txt -n 15
```


