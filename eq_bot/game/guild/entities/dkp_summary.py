from dateutil.parser import parse

from datetime import datetime
from dataclasses import dataclass

from typing import List

from game.guild.entities.guild_member_dkp import GuildMemberDkp

@dataclass
class DkpSummary:
    taken_at: datetime
    as_of_date_utc: datetime
    guild_members: List[GuildMemberDkp]

    def to_json(self):
        result = dict(vars(self))
        # TODO: Find an object->json serialization pattern where
        # we don't have to explicitly map objects
        result['guild_members'] = [member.to_json() for member in self.guild_members]
        return result

    @staticmethod
    def from_json(json):
        return DkpSummary(
            taken_at=parse(json["taken_at"]),
            as_of_date_utc=parse(json["as_of_date_utc"]),
            guild_members=[GuildMemberDkp.from_json(member) for member in json["guild_members"]])
