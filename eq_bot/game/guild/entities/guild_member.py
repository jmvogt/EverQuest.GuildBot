from datetime import datetime
from dataclasses import dataclass
from game.entities.player import Player

@dataclass
class GuildMember:
    name: str
    class_type: str
    level: int
    last_seen_by_bot: datetime
    last_seen_on: datetime
    rank: str
    is_alt: bool
    zone: str
    public_note: str
    is_online: bool

    def print(self):
        print(vars(self))
