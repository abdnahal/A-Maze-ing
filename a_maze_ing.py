"""Main entry point for the A-Maze-ing maze generator application.

This module provides an interactive terminal-based interface for generating,
displaying, and navigating through procedurally generated mazes with optional
pattern generation and path visualization.
"""

import sys
from mazegen import ConfigParser, Maze, MazeGenerator, PathFinder, MazeDisplay


def clear_screen():
    """Clear the terminal screen and move cursor to home position."""
    print("\033[2J\033[H", end="")


def main():
    """Main application loop for the maze generator.

    Reads configuration, generates a maze, finds a path, and provides
    an interactive interface for displaying and manipulating the maze.

    Raises:
        SystemExit: If incorrect command line arguments are provided.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <config_file>")
        sys.exit(1)

    config = ConfigParser(sys.argv[1])

    width = config.get_int("WIDTH")
    height = config.get_int("HEIGHT")
    entry = config.get_tuple("ENTRY")
    exit_pos = config.get_tuple("EXIT")
    output_file = config.get("OUTPUT_FILE")
    seed = config.get_int("SEED") if config.get("SEED") else None
    perfect = config.get_bool("PERFECT")

    if width < 8 or height < 5:
        print(
            "Error: maze dimensions too small for 42 pattern, maze creation will proceed without 42 pattern..."
        )
    maze = Maze(width, height, entry, exit_pos)
    generator = MazeGenerator(maze, seed=seed)
    pathfinder = PathFinder(maze)

    generator.generate(perfect=perfect)

    display = MazeDisplay(maze, set(generator.pattern_42_cells))
    path = pathfinder.find_path(entry, exit_pos)

    if path is None:
        print("Error: No path found from entry to exit!")
        sys.exit(1)

    display.set_path(path)
    maze.to_file(output_file, path)
    print(f"Maze saved to {output_file}\n")

    while True:
        clear_screen()
        display.display()

        print("\n" + "=" * 50)
        print("Commands:")
        print("  [p] Show/Hide path")
        print("  [4] Show/Hide '42' pattern")
        print("  [n] Generate new maze")
        print("  [c] Change wall color")
        print("  [2] Change '42' pattern color")
        print("  [q] Quit")
        print("=" * 50)
        try:
            choice = input("Your choice: ").lower().strip()

            if choice == "p":
                display.toggle_path()

            elif choice == "4":
                display.toggle_pattern()

            elif choice == "n":
                print("Generating new maze...")
                generator.generate(perfect=perfect)
                path = pathfinder.find_path(entry, exit_pos)
                if path:
                    display.set_path(path)
                    maze.to_file(output_file, path)
                    print(f"New maze saved to {output_file}")
                else:
                    print("Error: No path found!")
                input("Press Enter to continue...")

            elif choice == "c":
                display.change_wall_color_interactive()
                input("Press Enter to continue...")

            elif choice == "2":
                display.change_pattern_color_interactive()
                input("Press Enter to continue...")

            elif choice == "q":
                print("Goodbye!")
                break

            else:
                print("Invalid choice!")
                input("Press Enter to continue...")
        except (EOFError, KeyboardInterrupt):
            print()
            return


if __name__ == "__main__":
    main()
