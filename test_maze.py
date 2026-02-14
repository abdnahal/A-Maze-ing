from mazegen import Maze, MazeGenerator, PathFinder, MazeDisplay


def test_basic():
    maze = Maze(width=10, height=10, entry=(0, 0), exit=(9, 9))
    generator = MazeGenerator(maze, seed=42)
    generator.generate()

    pathfinder = PathFinder(maze)
    path = pathfinder.find_path(maze.entry, maze.exit)

    assert path is not None
    assert len(path) > 0

    print("✓ Basic maze generation test passed")


def test_hex_encoding():
    maze = Maze(width=5, height=5, entry=(0, 0), exit=(4, 4))
    generator = MazeGenerator(maze, seed=123)
    generator.generate()

    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            hex_val = cell.to_hex()
            assert hex_val in "0123456789ABCDEF"

    print("✓ Hex encoding test passed")


def test_pathfinding():
    maze = Maze(width=8, height=6, entry=(0, 0), exit=(7, 5))
    generator = MazeGenerator(maze, seed=999)
    generator.generate()

    pathfinder = PathFinder(maze)
    path = pathfinder.find_path(maze.entry, maze.exit)

    assert path is not None

    x, y = maze.entry
    for direction in path:
        if direction == "N":
            y -= 1
        elif direction == "E":
            x += 1
        elif direction == "S":
            y += 1
        elif direction == "W":
            x -= 1

    assert (x, y) == maze.exit

    print("✓ Pathfinding test passed")


if __name__ == "__main__":
    test_basic()
    test_hex_encoding()
    test_pathfinding()
    print("\n✅ All tests passed!")
