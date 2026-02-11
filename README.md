*This project has been created as part of the 42 curriculum by <mberouak>[<zahraka>].*

# A-Maze-ing - Maze Generator

## Description

A-Maze-ing is a Python maze generator that creates perfect mazes using the recursive backtracker algorithm. It includes a terminal-based ASCII visualization with path-finding capabilities and an interactive interface.

**Features:**
- Random maze generation with reproducible seeds
- Perfect mazes (exactly one path between entry and exit)
- Shortest path finding using BFS
- Interactive terminal display with colors
- "42" pattern easter egg embedded in mazes
- Export to hexadecimal format

## Instructions

### Installation

```bash
make install
```

### Running the Program

```bash
python3 a_maze_ing.py config.txt
```

Or use the Makefile:

```bash
make run
```

### Interactive Commands

Once the program is running:
- **p** - Toggle path visibility (show/hide solution)
- **n** - Generate a new maze
- **c** - Change wall colors
- **q** - Quit

### Configuration File Format

The config file uses `KEY=VALUE` format:

```
# Comments start with #
WIDTH=20          # Maze width in cells
HEIGHT=15         # Maze height in cells
ENTRY=0,0         # Entry coordinates (x,y)
EXIT=19,14        # Exit coordinates (x,y)
OUTPUT_FILE=maze.txt  # Output filename
PERFECT=True      # Perfect maze (one path only)
SEED=42           # Random seed for reproducibility
```

### Output File Format

The output file contains:
1. Hexadecimal grid (one digit per cell)
2. Empty line
3. Entry coordinates
4. Exit coordinates
5. Solution path (sequence of N/E/S/W)

**Hexadecimal Encoding:**
- Bit 0 (LSB): North wall
- Bit 1: East wall
- Bit 2: South wall
- Bit 3: West wall

Example: `F` = 1111 binary = all walls closed

## Resources

### Maze Generation Algorithms
- [Recursive Backtracker (DFS)](https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker)
- [Maze Generation Algorithms Overview](https://www.jamisbuck.org/mazes/)

### Pathfinding
- [Breadth-First Search](https://en.wikipedia.org/wiki/Breadth-first_search)

### Python Resources
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [ANSI Color Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)

### AI Usage

AI was used for:
- Learning and understanding maze generation algorithms
- Code structure and best practices guidance
- Helping with debugging bitwise operations
- Understanding the hexadecimal encoding format
- Writing documentation templates
- Giving suggestions for online sources to read from

All code was written with full understanding and explanation of each component.

## Maze Generation Algorithm

**Algorithm:** Recursive Backtracker (Depth-First Search)

**Why this algorithm:**
- Guarantees perfect mazes (single path between any two points)
- Easy to understand and implement
- Creates interesting, twisty corridors
- Naturally handles the entry/exit constraint

**How it works:**
1. Start at entry point, mark as visited
2. Choose random unvisited neighbor
3. Remove wall between current and neighbor
4. Recursively visit neighbor
5. Backtrack when stuck
6. Continue until all cells visited

## Reusable Code

The `mazegen` package can be imported and reused:

```python
from mazegen import Maze, MazeGenerator, PathFinder

# Create maze
maze = Maze(width=10, height=10, entry=(0,0), exit=(9,9))

# Generate it
generator = MazeGenerator(maze, seed=42)
generator.generate()

# Find path
finder = PathFinder(maze)
path = finder.find_path(maze.entry, maze.exit)

# Access maze structure
cell = maze.get_cell(5, 5)
print(cell.to_hex())
```

## Project Structure

```
maze_project/
├── mazegen/              # Reusable package
│   ├── __init__.py
│   ├── cell.py           # Cell data structure
│   ├── maze.py           # Maze grid container
│   ├── generator.py      # Maze generation algorithm
│   ├── pathfinder.py     # BFS pathfinding
│   ├── display.py        # Terminal visualization
│   └── config_parser.py  # Config file parser
├── a_maze_ing.py         # Main program
├── config.txt            # Default configuration
├── Makefile              # Build automation
├── .gitignore
└── README.md
```

## Team & Project Management

**Team Members:**
- [mberouak, zahraka] - All components

**Roles:**
- Algorithm implementation
- Display system
- File I/O
- Testing and debugging

**Planning:**
- Initial: 5 days estimated
- Actual: Completed in planned time
- Iterations: 3 major revisions

**What worked well:**
- Breaking down into small, testable components
- Building data structures before algorithms
- Testing each component independently

**What could be improved:**
- Earlier consideration of the "42" pattern requirement
- More comprehensive error handling
- Additional maze generation algorithms

**Tools Used:**
- Git for version control
- mypy for type checking
- flake8 for code style
