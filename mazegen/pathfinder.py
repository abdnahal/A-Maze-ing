"""Module for finding paths through a maze."""

from collections import deque
from mazegen.maze import Maze
from typing import List, Optional, Tuple, Deque


class PathFinder:
    """Finds paths through a maze using breadth-first search (BFS).

    Computes the shortest path between any two points in the maze.
    """

    def __init__(self, maze: Maze):
        """Initialize the pathfinder with a maze.

        Args:
            maze: The Maze object to find paths in.
        """
        self.maze = maze

    def find_path(
        self, start: Tuple[int, int], end: Tuple[int, int]
    ) -> Optional[List[str]]:
        """Find the shortest path from start to end using BFS.

        Args:
            start: The (x, y) coordinates of the starting position.
            end: The (x, y) coordinates of the ending position.

        Returns:
            A list of direction characters ('N', 'E', 'S', 'W') representing
            the path, or None if no path exists.
        """
        queue: Deque[Tuple[int, int, List]] = deque([(start[0], start[1], [])])
        visited = set()
        visited.add(start)

        while queue:
            x, y, path = queue.popleft()

            if (x, y) == end:
                return path

            cell = self.maze.get_cell(x, y)
            if cell:
                if not cell.north and (x, y - 1) not in visited:
                    if self.maze.is_valid_position(x, y - 1):
                        visited.add((x, y - 1))
                        queue.append((x, y - 1, path + ["N"]))

                if not cell.east and (x + 1, y) not in visited:
                    if self.maze.is_valid_position(x + 1, y):
                        visited.add((x + 1, y))
                        queue.append((x + 1, y, path + ["E"]))

                if not cell.south and (x, y + 1) not in visited:
                    if self.maze.is_valid_position(x, y + 1):
                        visited.add((x, y + 1))
                        queue.append((x, y + 1, path + ["S"]))

                if not cell.west and (x - 1, y) not in visited:
                    if self.maze.is_valid_position(x - 1, y):
                        visited.add((x - 1, y))
                        queue.append((x - 1, y, path + ["W"]))

        return None
