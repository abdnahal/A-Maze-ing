from collections import deque
from mazegen.maze import Maze
from typing import List, Optional, Tuple

class PathFinder:
    def __init__(self, maze: Maze):
        self.maze = maze
    
    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[str]]:
        queue = deque([(start[0], start[1], [])])
        visited = set()
        visited.add(start)
        
        while queue:
            x, y, path = queue.popleft()
            
            if (x, y) == end:
                return path
            
            cell = self.maze.get_cell(x, y)
            
            if not cell.north and (x, y-1) not in visited:
                if self.maze.is_valid_position(x, y-1):
                    visited.add((x, y-1))
                    queue.append((x, y-1, path + ['N']))
            
            if not cell.east and (x+1, y) not in visited:
                if self.maze.is_valid_position(x+1, y):
                    visited.add((x+1, y))
                    queue.append((x+1, y, path + ['E']))
            
            if not cell.south and (x, y+1) not in visited:
                if self.maze.is_valid_position(x, y+1):
                    visited.add((x, y+1))
                    queue.append((x, y+1, path + ['S']))
            
            if not cell.west and (x-1, y) not in visited:
                if self.maze.is_valid_position(x-1, y):
                    visited.add((x-1, y))
                    queue.append((x-1, y, path + ['W']))
        
        return None
