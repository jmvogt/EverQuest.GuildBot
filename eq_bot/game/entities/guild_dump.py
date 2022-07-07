from dataclasses import dataclass
from typing import List
from datetime import datetime

from game.entities.guild_member import GuildMember

@dataclass
class GuildDump:
    members: List[GuildMember]
    taken_at: datetime

    def print(self):
        print(f'Dump taken at {self.taken_at.isoformat()}')
        print('-------- Members --------')
        for member in self.members:
            member.print()
        print('-------------------------\n')
