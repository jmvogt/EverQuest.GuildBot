from datetime import datetime

from game.guild.entities.guild_dump import GuildDump
from game.guild.entities.guild_dump_differential import GuildDumpDifferential

from utils.config import get_config


DAYS_UNTIL_INACTIVE=get_config('guild_tracking.in_game_dump.days_until_inactive', 30)


def build_differential(from_dump: GuildDump, to_dump: GuildDump) -> GuildDumpDifferential:
    new_members = []
    left_members = []
    inactive_members = []
    logged_on = []
    logged_off = []

    current_time = datetime.now()

    for member in to_dump.members:
        from_member = next((x for x in from_dump.members if x.name == member.name), None)
        if not from_member:
            new_members.append(member)
        else:
            if not from_member.is_online and member.is_online:
                logged_on.append(member)
            if from_member.is_online and not member.is_online:
                logged_off.append(member)
            # Only add to off member list if they weren't off duty in the previous run but are now
            if (current_time - member.last_seen_on).days > DAYS_UNTIL_OFF_DUTY and not\
                (current_time - from_member.last_seen_on).days > DAYS_UNTIL_OFF_DUTY:
                inactive_members.append(member)

    
    for member in from_dump.members:
        to_member = next((x for x in to_dump.members if x.name == member.name), None)
        if not to_member:
            left_members.append(member)
    
    return GuildDumpDifferential(
        new_members=new_members,
        left_members=left_members,
        inactive_members=inactive_members,
        logged_on=logged_on,
        logged_off=logged_off,
        delta_time=to_dump.taken_at - from_dump.taken_at)
