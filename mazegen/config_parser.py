class ConfigParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.config = {}
        self.parse()
    
    def parse(self) -> None:
        try:
            with open(self.filepath, 'r') as f:
                for line in f:
                    line = line.strip()
                    
                    if not line:
                        continue
                    
                    if line.startswith('#'):
                        continue
                    
                    if '=' in line:
                        parts = line.split('=', 1)
                        key = parts[0].strip()
                        value = parts[1].strip()
                        self.config[key] = value
        
        except FileNotFoundError:
            print(f"Error: Config file '{self.filepath}' not found!")
            raise
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)
    
    def get_int(self, key: str) -> int:
        value = self.config.get(key)
        if value is None:
            raise KeyError(f"Missing key: {key}")
        return int(value)
    
    def get_bool(self, key: str) -> bool:
        value = self.config.get(key)
        if value is None:
            raise KeyError(f"Missing key: {key}")
        return value.lower() == 'true'
    
    def get_tuple(self, key: str) -> tuple[int, int]:
        value = self.config.get(key)
        if value is None:
            raise KeyError(f"Missing key: {key}")
        parts = value.split(',')
        return (int(parts[0].strip()), int(parts[1].strip()))
