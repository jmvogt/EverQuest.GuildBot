from dataclasses import dataclass

@dataclass
class Player:
    name: str
    class_type: str
    level: int

@dataclass
class CurrentPlayer:
    name: str
    server: str
