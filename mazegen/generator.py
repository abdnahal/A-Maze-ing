import random
from mazegen.maze import Maze
from typing import List, Tuple

class MazeGenerator:
    def __init__(self, maze: Maze, seed: int = None):
        self.maze = maze
        if seed is not None:
            random.seed(seed)
        self.visited = [[False for _ in range(maze.width)] for _ in range(maze.height)]
        self.pattern_42_cells = []
    
    def generate(self, perfect: bool = True) -> None:
        start_x, start_y = self.maze.entry
        self.visited = [[False for _ in range(self.maze.width)] for _ in range(self.maze.height)]
        self.recursive_backtrack(start_x, start_y)
        
        if not perfect:
            self.add_loops()
        
        self.add_pattern_42_safe()
    
    def recursive_backtrack(self, x: int, y: int) -> None:
        self.visited[y][x] = True
        neighbors = self.get_unvisited_neighbors(x, y)
        random.shuffle(neighbors)
        
        for next_x, next_y, direction in neighbors:
            if not self.visited[next_y][next_x]:
                self.remove_wall_between(x, y, next_x, next_y, direction)
                self.recursive_backtrack(next_x, next_y)
    
    def get_unvisited_neighbors(self, x: int, y: int) -> List[Tuple[int, int, str]]:
        neighbors = []
        
        if y > 0 and not self.visited[y-1][x]:
            neighbors.append((x, y-1, 'north'))
        
        if x < self.maze.width - 1 and not self.visited[y][x+1]:
            neighbors.append((x+1, y, 'east'))
        
        if y < self.maze.height - 1 and not self.visited[y+1][x]:
            neighbors.append((x, y+1, 'south'))
        
        if x > 0 and not self.visited[y][x-1]:
            neighbors.append((x-1, y, 'west'))
        
        return neighbors
    
    def remove_wall_between(self, x1: int, y1: int, x2: int, y2: int, direction: str) -> None:
        cell1 = self.maze.get_cell(x1, y1)
        cell2 = self.maze.get_cell(x2, y2)
        
        if direction == 'north':
            cell1.north = False
            cell2.south = False
        elif direction == 'east':
            cell1.east = False
            cell2.west = False
        elif direction == 'south':
            cell1.south = False
            cell2.north = False
        elif direction == 'west':
            cell1.west = False
            cell2.east = False
    
    def add_loops(self, loop_percentage: float = 0.15) -> None:
        total_cells = self.maze.width * self.maze.height
        walls_to_remove = int(total_cells * loop_percentage)
        
        removed = 0
        attempts = 0
        max_attempts = walls_to_remove * 10
        
        while removed < walls_to_remove and attempts < max_attempts:
            attempts += 1
            x = random.randint(0, self.maze.width - 1)
            y = random.randint(0, self.maze.height - 1)
            cell = self.maze.get_cell(x, y)
            
            if not cell:
                continue
            
            direction = random.choice(['north', 'east', 'south', 'west'])
            
            if direction == 'north' and y > 0 and cell.north:
                neighbor = self.maze.get_cell(x, y - 1)
                cell.north = False
                neighbor.south = False
                removed += 1
            elif direction == 'east' and x < self.maze.width - 1 and cell.east:
                neighbor = self.maze.get_cell(x + 1, y)
                cell.east = False
                neighbor.west = False
                removed += 1
            elif direction == 'south' and y < self.maze.height - 1 and cell.south:
                neighbor = self.maze.get_cell(x, y + 1)
                cell.south = False
                neighbor.north = False
                removed += 1
            elif direction == 'west' and x > 0 and cell.west:
                neighbor = self.maze.get_cell(x - 1, y)
                cell.west = False
                neighbor.east = False
                removed += 1
    
    def add_pattern_42_safe(self) -> None:
        pattern = [
            [1, 0, 0, 1, 0, 1, 1, 1],
            [1, 0, 0, 1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0, 1, 1, 1],
            [0, 0, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 1]
        ]
        
        pattern_height = len(pattern)
        pattern_width = len(pattern[0])
        
        if self.maze.height < pattern_height + 2 or self.maze.width < pattern_width + 2:
            return
        
        from mazegen.pathfinder import PathFinder
        pathfinder = PathFinder(self.maze)
        solution_path = pathfinder.find_path(self.maze.entry, self.maze.exit)
        
        if not solution_path:
            return
        
        solution_cells = set()
        x, y = self.maze.entry
        solution_cells.add((x, y))
        for direction in solution_path:
            if direction == 'N':
                y -= 1
            elif direction == 'E':
                x += 1
            elif direction == 'S':
                y += 1
            elif direction == 'W':
                x -= 1
            solution_cells.add((x, y))
        
        max_attempts = 50
        for attempt in range(max_attempts):
            start_x = random.randint(1, self.maze.width - pattern_width - 1)
            start_y = random.randint(1, self.maze.height - pattern_height - 1)
            
            pattern_cells = []
            valid = True
            
            for py in range(pattern_height):
                for px in range(pattern_width):
                    if pattern[py][px] == 1:
                        cell_x = start_x + px
                        cell_y = start_y + py
                        
                        if (cell_x, cell_y) in solution_cells:
                            valid = False
                            break
                        
                        pattern_cells.append((cell_x, cell_y))
                
                if not valid:
                    break
            
            if valid and len(pattern_cells) > 0:
                for cell_x, cell_y in pattern_cells:
                    cell = self.maze.get_cell(cell_x, cell_y)
                    if cell:
                        cell.north = True
                        cell.east = True
                        cell.south = True
                        cell.west = True
                        self.pattern_42_cells.append((cell_x, cell_y))
                return

