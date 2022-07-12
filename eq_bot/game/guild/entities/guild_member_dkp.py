from dataclasses import dataclass

@dataclass
class GuildMemberDkp:
    current_dkp: float
    character_id: int
    character_name: str
    character_class: str
    character_rank: str
    character_status: int
    attended_ticks_30: float
    total_ticks_30: float
    calculated_30: float
    attended_ticks_60: float
    total_ticks_60: float
    calculated_60: float
    attended_ticks_90: float
    total_ticks_90: float
    calculated_90: float
    attended_ticks_life: float
    total_ticks_life: float
    calculated_life: float

    def to_json(self):
        return vars(self)

    @staticmethod
    def from_json(json):
        return GuildMemberDkp(**json)
