from dataclasses import dataclass
from datetime import timedelta

from typing import List

from game.guild.entities.guild_member_dkp import GuildMemberDkp

@dataclass
class DkpSummaryDifferential:
    offduty_members: List[GuildMemberDkp]
    delta_time: timedelta

    @property
    def has_differences(self):
        return len(self.offduty_members) > 0

    def print(self):
        print('-------- Off Duty Members --------')
        for member in self.offduty_members:
            print (member.__dict__)
        print('\n')
