from dataclasses import dataclass
from datetime import timedelta

from typing import List

from game.guild.entities.guild_member import GuildMember

@dataclass
class GuildDumpDifferential:
    new_members: List[GuildMember]
    left_members: List[GuildMember]
    offduty_members: List[GuildMember]
    logged_on: List[GuildMember]
    logged_off: List[GuildMember]
    delta_time: timedelta

    @property
    def has_differences(self):
        return len(self.new_members) > 0 or \
            len(self.left_members) > 0 or \
            len(self.offduty_members) > 0 or \
            len(self.logged_on) > 0 or \
            len(self.logged_off) > 0

    def print(self):
        print('-------- New Members --------')
        for member in self.new_members:
            member.print()
        print('\n')

        print('-------- Quitting Members --------')
        for member in self.left_members:
            member.print()
        print('\n')

        print('-------- Off Duty Members --------')
        for member in self.offduty_members:
            member.print()
        print('\n')

        print('-------- Logged On Members --------')
        for member in self.logged_on:
            member.print()
        print('\n')

        print('-------- Logged Off Members --------')
        for member in self.logged_off:
            member.print()
        print('\n')
