from mazegen.cell import Cell
from typing import Optional, List

class Maze:
    def __init__(self, width: int, height: int, 
                 entry: tuple[int, int], exit: tuple[int, int]):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
    
    def is_valid_position(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height
    
    def get_cell(self, x: int, y: int) -> Optional[Cell]:
        if not self.is_valid_position(x, y):
            return None
        return self.grid[y][x]
    
    def set_cell(self, x: int, y: int, cell: Cell) -> None:
        if self.is_valid_position(x, y):
            self.grid[y][x] = cell
    
    def to_file(self, filepath: str, path: List[str]) -> None:
        with open(filepath, 'w') as f:
            for y in range(self.height):
                for x in range(self.width):
                    f.write(self.get_cell(x, y).to_hex())
                f.write('\n')
            
            f.write('\n')
            f.write(f'{self.entry[0]},{self.entry[1]}\n')
            f.write(f'{self.exit[0]},{self.exit[1]}\n')
            f.write(''.join(path) + '\n')
