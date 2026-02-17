"""Module for representing and manipulating a maze grid."""

from mazegen.cell import Cell
from typing import Optional, List


class Maze:
    """Represents a rectangular maze grid composed of cells with walls.

    Manages the maze structure including dimensions, entry/exit points,
    and individual cell states.
    """

    def __init__(
        self, width: int, height: int, entry:
        tuple[int, int], exit: tuple[int, int]
    ):
        """Initialize a maze with specified dimensions and entry/exit points.

        Args:
            width: The width of the maze in cells.
            height: The height of the maze in cells.
            entry: The (x, y) coordinates of the maze entry point.
            exit: The (x, y) coordinates of the maze exit point.
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if the given coordinates are within the maze bounds.

        Args:
            x: The x-coordinate to check.
            y: The y-coordinate to check.

        Returns:
            True if the position is within the maze, False otherwise.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        """Retrieve a cell at the specified coordinates.

        Args:
            x: The x-coordinate of the cell.
            y: The y-coordinate of the cell.

        Returns:
            The Cell object at the position, or None if out of bounds.
        """
        if not self.is_valid_position(x, y):
            return None
        return self.grid[y][x]

    def set_cell(self, x: int, y: int, cell: Cell) -> None:
        """Set a cell at the specified coordinates.

        Args:
            x: The x-coordinate of the cell.
            y: The y-coordinate of the cell.
            cell: The Cell object to place at this position.
        """
        if self.is_valid_position(x, y):
            self.grid[y][x] = cell

    def to_file(self, filepath: str, path: List[str]) -> None:
        """Write the maze to a file in hex-encoded format.

        Args:
            filepath: The path where the maze file will be written.
            path: List of direction characters representing the solution path.
        """
        with open(filepath, "w") as f:
            for y in range(self.height):
                for x in range(self.width):
                    cell = self.get_cell(x, y)
                    if cell:
                        f.write(cell.to_hex())
                f.write("\n")

            f.write("\n")
            f.write(f"{self.entry[0]},{self.entry[1]}\n")
            f.write(f"{self.exit[0]},{self.exit[1]}\n")
            f.write("".join(path) + "\n")
