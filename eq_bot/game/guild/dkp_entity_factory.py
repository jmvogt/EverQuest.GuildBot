from datetime import datetime
from dateutil.parser import parse

from game.guild.entities.guild_member_dkp import GuildMemberDkp
from game.guild.entities.dkp_summary import DkpSummary


def build_member_dkp_from_gateway(member_json):
    return GuildMemberDkp(
        current_dkp=member_json["CurrentDKP"],
        character_id=member_json["IdCharacter"],
        character_name=member_json["CharacterName"],
        character_class=member_json["CharacterClass"],
        character_rank=member_json["CharacterRank"],
        character_status=member_json["CharacterStatus"],
        attended_ticks_30=member_json["AttendedTicks_30"],
        total_ticks_30=member_json["TotalTicks_30"],
        calculated_30=member_json["Calculated_30"],
        attended_ticks_60=member_json["AttendedTicks_60"],
        total_ticks_60=member_json["TotalTicks_60"],
        calculated_60=member_json["Calculated_60"],
        attended_ticks_90=member_json["AttendedTicks_90"],
        total_ticks_90=member_json["TotalTicks_90"],
        calculated_90=member_json["Calculated_90"],
        attended_ticks_life=member_json["AttendedTicks_Life"],
        total_ticks_life=member_json["TotalTicks_Life"],
        calculated_life=member_json["Calculated_Life"])

def build_summary_from_gateway(response_json):
    return DkpSummary(
        taken_at=datetime.now(),
        as_of_date_utc=parse(response_json["AsOfDate"]),
        guild_members=[build_member_dkp_from_gateway(member_model) for member_model in response_json["Models"]])
