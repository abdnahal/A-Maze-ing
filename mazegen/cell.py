"""Module for representing individual maze cells and their wall states."""


class Cell:
    """Represents a single cell in a maze with walls on four sides.

    A cell has four boolean flags representing walls in each cardinal
    direction.
    Walls are represented as True (wall exists) or False (wall is open).
    """

    def __init__(
        self,
        north: bool = True,
        east: bool = True,
        south: bool = True,
        west: bool = True,
    ):
        """Initialize a cell with walls in specified directions.

        Args:
            north: Whether there is a wall to the north (default: True).
            east: Whether there is a wall to the east (default: True).
            south: Whether there is a wall to the south (default: True).
            west: Whether there is a wall to the west (default: True).
        """
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def to_hex(self) -> str:
        """Convert cell wall state to a single hexadecimal character.

        Returns:
            A hex string (0-F) representing the wall state.
            Each bit represents a wall: N=1, E=2, S=4, W=8.
        """
        value = (
            int(self.north)
            + int(self.east) * 2
            + int(self.south) * 4
            + int(self.west) * 8
        )
        return format(value, "X")

    def from_hex(self, hex_char: str) -> None:
        """Set cell wall state from a hexadecimal character.

        Args:
            hex_char: A single hex character (0-F) representing wall state.
                Each bit represents a wall: N=1, E=2, S=4, W=8.
        """
        num = int(hex_char, 16)
        self.north = bool(num & 1)
        self.east = bool((num >> 1) & 1)
        self.south = bool((num >> 2) & 1)
        self.west = bool((num >> 3) & 1)

    def __str__(self) -> str:
        """Return a string representation of the cell's wall state.

        Returns:
            A formatted string showing the state of all four walls.
        """
        return f"Cell(N={self.north}, E={self.east}, S={self.south},\
        W={self.west})"
