"""Module for generating mazes using recursive backtracking algorithm."""

import random
from mazegen.maze import Maze
from typing import List, Tuple, Optional
import sys


class MazeGenerator:
    """Generates mazes using the recursive backtracking algorithm.

    Supports generation of perfect mazes (trees) and
    imperfect mazes (with loops),
    and can add decorative '42' patterns throughout the maze.
    """

    def __init__(self, maze: Maze, seed: Optional[int] = None):
        """Initialize the maze generator.

        Args:
            maze: The Maze object to generate.
            seed: Optional random seed for reproducible generation.
        """
        self.maze = maze
        self.seed = seed
        self.visited = [[False for _ in range(maze.width)]
                        for _ in range(maze.height)]
        self.pattern_42_cells: List[Tuple[int, int]] = []

    def generate(self, perfect: bool = True) -> None:
        """Generate the maze.

        Args:
            perfect: If True, generates a perfect maze (tree structure).
                    If False, adds loops to create a more complex maze.
        """
        self.maze.reset()
        self.pattern_42_cells = []

        # Re-apply seed on every generation so seeded runs are always identical
        if self.seed is not None:
            random.seed(self.seed)
        else:
            random.seed()

        # Reset visited grid
        self.visited = [
            [False for _ in range(self.maze.width)]
            for _ in range(self.maze.height)
        ]

        # Place pattern FIRST so maze generates around it
        self.place_pattern_center()

        start_x, start_y = self.maze.entry
        end_x, end_y = self.maze.exit
        if start_x >= self.maze.width or start_y >= self.maze.height:
            print("Invalid Entry dimensions")
            sys.exit(1)
        if end_x >= self.maze.width or end_y >= self.maze.height:
            print("Invalid Exit dimensions")
            sys.exit(1)
        self.recursive_backtrack(start_x, start_y)

        if not perfect:
            self.add_loops()

    def place_pattern_center(self) -> None:
        """Place '42' pattern as obstacles in the center of the maze."""
        pattern = [
            [1, 0, 0, 1, 0, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 1],
        ]

        pattern_height = len(pattern)
        pattern_width = len(pattern[0])

        # Calculate center position
        start_x = (self.maze.width - pattern_width) // 2
        start_y = (self.maze.height - pattern_height) // 2

        # Ensure maze is big enough
        if start_x < 0 or start_y < 0:
            return

        # Place the pattern
        for py in range(pattern_height):
            for px in range(pattern_width):
                if pattern[py][px] == 1:
                    cell_x = start_x + px
                    cell_y = start_y + py

                    if self.maze.is_valid_position(cell_x, cell_y):
                        # Mark as visited so generator avoids it
                        self.visited[cell_y][cell_x] = True

                        # Add to pattern list for display
                        self.pattern_42_cells.append((cell_x, cell_y))

    def recursive_backtrack(self, x: int, y: int) -> None:
        """Generate maze using recursive backtracking from a starting cell.

        Args:
            x: The x-coordinate of the current cell.
            y: The y-coordinate of the current cell.
        """
        self.visited[y][x] = True
        neighbors = self.get_unvisited_neighbors(x, y)
        random.shuffle(neighbors)

        for next_x, next_y, direction in neighbors:
            if not self.visited[next_y][next_x]:
                self.remove_wall_between(x, y, next_x, next_y, direction)
                self.recursive_backtrack(next_x, next_y)

    def get_unvisited_neighbors(self, x: int,
                                y: int) -> List[Tuple[int, int, str]]:
        """Get all unvisited neighbor cells in cardinal directions.

        Args:
            x: The x-coordinate of the current cell.
            y: The y-coordinate of the current cell.

        Returns:
            List of tuples (x, y, direction) for each unvisited neighbor.
        """
        neighbors = []

        if y > 0 and not self.visited[y - 1][x]:
            neighbors.append((x, y - 1, "north"))

        if x < self.maze.width - 1 and not self.visited[y][x + 1]:
            neighbors.append((x + 1, y, "east"))

        if y < self.maze.height - 1 and not self.visited[y + 1][x]:
            neighbors.append((x, y + 1, "south"))

        if x > 0 and not self.visited[y][x - 1]:
            neighbors.append((x - 1, y, "west"))

        return neighbors

    def remove_wall_between(
        self, x1: int, y1: int, x2: int, y2: int, direction: str
    ) -> None:
        """Remove the wall between two adjacent cells.

        Args:
            x1: The x-coordinate of the first cell.
            y1: The y-coordinate of the first cell.
            x2: The x-coordinate of the second cell.
            y2: The y-coordinate of the second cell.
            direction: The direction from cell1 to cell2
            ('north', 'east', 'south', 'west').
        """
        cell1 = self.maze.get_cell(x1, y1)
        cell2 = self.maze.get_cell(x2, y2)
        if cell1 and cell2:
            if direction == "north":
                cell1.north = False
                cell2.south = False
            elif direction == "east":
                cell1.east = False
                cell2.west = False
            elif direction == "south":
                cell1.south = False
                cell2.north = False
            elif direction == "west":
                cell1.west = False
                cell2.east = False

    def add_loops(self, loop_percentage: float = 0.15) -> None:
        """Add loops to the maze by randomly removing walls.

        Creates cycles in the maze structure, making it more complex and
        less tree-like.

        Args:
            loop_percentage: The percentage of walls to remove as a fraction
                           of total cells (default: 0.15 or 15%).
        """
        total_cells = self.maze.width * self.maze.height
        walls_to_remove = int(total_cells * loop_percentage)
        pattern_set = set(self.pattern_42_cells)

        removed = 0
        attempts = 0
        max_attempts = walls_to_remove * 10

        while removed < walls_to_remove and attempts < max_attempts:
            attempts += 1
            x = random.randint(0, self.maze.width - 1)
            y = random.randint(0, self.maze.height - 1)

            if (x, y) in pattern_set:
                continue

            cell = self.maze.get_cell(x, y)
            if not cell:
                continue

            direction = random.choice(["north", "east", "south", "west"])
            height = self.maze.height
            if direction == "north" and y > 0 and cell.north:
                if (x, y - 1) in pattern_set:
                    continue
                neighbor = self.maze.get_cell(x, y - 1)
                if neighbor:
                    cell.north = False
                    neighbor.south = False
                    removed += 1
            elif direction == "east" and x < self.maze.width - 1 and cell.east:
                if (x + 1, y) in pattern_set:
                    continue
                neighbor = self.maze.get_cell(x + 1, y)
                if neighbor:
                    cell.east = False
                    neighbor.west = False
                    removed += 1
            elif direction == "south" and y < height - 1 and cell.south:
                if (x, y + 1) in pattern_set:
                    continue
                neighbor = self.maze.get_cell(x, y + 1)
                if neighbor:
                    cell.south = False
                    neighbor.north = False
                    removed += 1
            elif direction == "west" and x > 0 and cell.west:
                if (x - 1, y) in pattern_set:
                    continue
                neighbor = self.maze.get_cell(x - 1, y)
                if neighbor:
                    cell.west = False
                    neighbor.east = False
                    removed += 1
