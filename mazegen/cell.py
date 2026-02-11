class Cell:
    def __init__(self, north: bool = True, east: bool = True, 
                 south: bool = True, west: bool = True):
        self.north = north
        self.east = east
        self.south = south
        self.west = west

    def to_hex(self) -> str:
        value = int(self.north) + int(self.east) * 2 + int(self.south) * 4 + int(self.west) * 8
        return format(value, 'X')
    
    def from_hex(self, hex_char: str) -> None:
        num = int(hex_char, 16)
        self.north = bool(num & 1)
        self.east = bool((num >> 1) & 1)
        self.south = bool((num >> 2) & 1)
        self.west = bool((num >> 3) & 1)
    
    def __str__(self) -> str:
        return f"Cell(N={self.north}, E={self.east}, S={self.south}, W={self.west})"
