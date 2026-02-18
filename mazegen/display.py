"""Module for rendering and displaying mazes in the terminal."""

from mazegen.maze import Maze
from typing import List, Set, Tuple, Optional


class MazeDisplay:
    """Renders and displays a maze in the terminal with colored elements.

    Supports displaying paths, patterns, entry/exit points, and interactive
    color customization.
    """

    WALL_COLOR = "\033[36m"
    PATH_COLOR = "\033[92m"
    ENTRY_COLOR = "\033[93m"
    EXIT_COLOR = "\033[91m"
    PATTERN_COLOR = "\033[45m"
    RESET = "\033[0m"

    def __init__(
        self, maze: Maze,
        pattern_42_cells: Optional[Set[Tuple[int, int]]] = None
    ):
        """Initialize the maze display.

        Args:
            maze: The Maze object to display.
            pattern_42_cells: Set of (x, y) coordinates for the '42' pattern
            cells.
        """
        self.maze = maze
        self.show_path = False
        self.show_pattern = True
        self.path_cells: Set[Tuple[int, int]] = set()
        self.pattern_42_cells = pattern_42_cells if pattern_42_cells else set()
        self.wall_color = self.WALL_COLOR
        self.path_color = self.PATH_COLOR
        self.entry_color = self.ENTRY_COLOR
        self.exit_color = self.EXIT_COLOR
        self.pattern_color = self.PATTERN_COLOR

    def set_pattern(self, pattern_cells: Set[Tuple[int, int]]) -> None:
        """Update the set of cells that form the '42' pattern.

        Args:
            pattern_cells: New set of (x, y) coordinates for the pattern.
        """
        self.pattern_42_cells = pattern_cells if pattern_cells else set()

    def set_path(self, path: List[str]) -> None:
        """Set the solution path to display.

        Args:
            path: List of direction characters ('N', 'E', 'S', 'W')
                 representing the path from entry to exit.
        """
        self.path_cells = set()
        x, y = self.maze.entry
        self.path_cells.add((x, y))

        for direction in path:
            if direction == "N":
                y -= 1
            elif direction == "E":
                x += 1
            elif direction == "S":
                y += 1
            elif direction == "W":
                x -= 1

            if self.maze.is_valid_position(x, y):
                self.path_cells.add((x, y))

    def toggle_path(self) -> None:
        """Toggle the visibility of the solution path."""
        self.show_path = not self.show_path

    def toggle_pattern(self) -> None:
        """Toggle the visibility of the '42' pattern."""
        self.show_pattern = not self.show_pattern

    def set_wall_color(self, color: str) -> None:
        """Set the ANSI color code for walls.

        Args:
            color: An ANSI color escape code.
        """
        self.wall_color = color

    def display(self) -> None:
        """Render and print the complete maze to the terminal."""
        self.print_top_border()

        for y in range(self.maze.height):
            self.print_row_cells(y)

            if y < self.maze.height - 1:
                self.print_row_divider(y)

        self.print_bottom_border()

    def print_top_border(self) -> None:
        """Print the top border of the maze."""
        line = f"{self.wall_color}┌"
        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, 0)
            if cell:
                if cell.north:
                    line += "───"
                else:
                    line += "   "

                if x < self.maze.width - 1:
                    if cell.east:
                        line += "┬"
                    else:
                        line += "─"

        line += f"┐{self.RESET}"
        print(line)

    def print_row_cells(self, y: int) -> None:
        """Print a row of maze cells with appropriate coloring.

        Args:
            y: The row index to print.
        """
        line = ""

        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, y)
            if cell:
                if cell.west:
                    line += f"{self.wall_color}│{self.RESET}"
                else:
                    line += " "

                if (x, y) == self.maze.entry:
                    line += f"{self.entry_color} S {self.RESET}"
                elif (x, y) == self.maze.exit:
                    line += f"{self.exit_color} E {self.RESET}"
                elif self.show_pattern and (x, y) in self.pattern_42_cells:
                    line += f"{self.pattern_color}   {self.RESET}"
                elif self.show_path and (x, y) in self.path_cells:
                    line += f"{self.path_color} · {self.RESET}"
                else:
                    line += "   "

        last_cell = self.maze.get_cell(self.maze.width - 1, y)
        if last_cell:
            if last_cell.east:
                line += f"{self.wall_color}│{self.RESET}"
            else:
                line += " "

            print(line)

    def print_row_divider(self, y: int) -> None:
        """Print a horizontal divider between maze rows.

        Args:
            y: The row index (used to determine wall positions).
        """
        line = f"{self.wall_color}├"
        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, y)
            if cell:
                if cell.south:
                    line += "───"
                else:
                    line += "   "
                if x < self.maze.width - 1:
                    line += "┼"
        line += f"┤{self.RESET}"
        print(line)

    def print_bottom_border(self) -> None:
        """Print the bottom border of the maze."""
        y = self.maze.height - 1
        line = f"{self.wall_color}└"

        for x in range(self.maze.width):
            cell = self.maze.get_cell(x, y)
            if cell:
                if cell.south:
                    line += "───"
                else:
                    line += "   "

                if x < self.maze.width - 1:
                    line += "┴"

        line += f"┘{self.RESET}"
        print(line)

    def show_color_options(self) -> dict:
        """Display available wall colors and return the color options.

        Returns:
            A dictionary mapping keys to (color_code, color_name) tuples.
        """
        colors = {
            "1": ("\033[31m", "Red"),
            "2": ("\033[32m", "Green"),
            "3": ("\033[33m", "Yellow"),
            "4": ("\033[34m", "Blue"),
            "5": ("\033[35m", "Magenta"),
            "6": ("\033[36m", "Cyan"),
            "7": ("\033[91m", "Bright Red"),
            "8": ("\033[92m", "Bright Green"),
            "9": ("\033[93m", "Bright Yellow"),
            "a": ("\033[94m", "Bright Blue"),
            "b": ("\033[95m", "Bright Magenta"),
            "c": ("\033[96m", "Bright Cyan"),
        }

        print("\nAvailable colors:")
        for key, (code, name) in colors.items():
            print(f"{key}: {code}{name}{self.RESET}")

        return colors

    def show_background_color_options(self) -> dict:
        """Display available background colors and return the options.

        Returns:
            A dictionary mapping keys to (color_code, color_name) tuples.
        """
        colors = {
            "1": ("\033[41m", "Red Background"),
            "2": ("\033[42m", "Green Background"),
            "3": ("\033[43m", "Yellow Background"),
            "4": ("\033[44m", "Blue Background"),
            "5": ("\033[45m", "Magenta Background"),
            "6": ("\033[46m", "Cyan Background"),
            "7": ("\033[101m", "Bright Red Background"),
            "8": ("\033[102m", "Bright Green Background"),
            "9": ("\033[103m", "Bright Yellow Background"),
            "a": ("\033[104m", "Bright Blue Background"),
            "b": ("\033[105m", "Bright Magenta Background"),
            "c": ("\033[106m", "Bright Cyan Background"),
        }

        print("\nAvailable background colors:")
        for key, (code, name) in colors.items():
            print(f"{key}: {code}   {self.RESET} {name}")

        return colors

    def change_wall_color_interactive(self) -> None:
        """Interactively prompt user to change the wall color."""
        colors = self.show_color_options()
        choice = input("\nChoose wall color (1-9, a-c): ").lower()

        if choice in colors:
            self.wall_color = colors[choice][0]
            print(f"Wall color changed to {colors[choice][1]}!")
        else:
            print("Invalid choice!")

    def change_pattern_color_interactive(self) -> None:
        """Interactively prompt user to change the pattern background color."""
        inp = "\nChoose pattern background color (1-9, a-c): "
        colors = self.show_background_color_options()
        choice = input(inp).lower()

        if choice in colors:
            self.pattern_color = colors[choice][0]
            print(f"Pattern color changed to {colors[choice][1]}!")
        else:
            print("Invalid choice!")
