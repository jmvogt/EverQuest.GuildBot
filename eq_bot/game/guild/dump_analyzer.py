from game.guild.entities.guild_dump import GuildDump
from game.guild.entities.guild_dump_differential import GuildDumpDifferential


def build_differential(from_dump: GuildDump, to_dump: GuildDump) -> GuildDumpDifferential:

    new_members = []
    left_members = []
    offduty_members = []
    logged_on = []
    logged_off = []

    for member in to_dump.members:
        from_member = next((x for x in from_dump.members if x.name == member.name), None)
        if not from_member:
            new_members.append(member)
        else:
            if not from_member.is_online and member.is_online:
                logged_on.append(member)
            if from_member.is_online and not member.is_online:
                logged_off.append(member)
    
    for member in from_dump.members:
        to_member = next((x for x in to_dump.members if x.name == member.name), None)
        if not to_member:
            left_members.append(member)
    
    return GuildDumpDifferential(
        new_members=new_members,
        left_members=left_members,
        offduty_members=offduty_members,
        logged_on=logged_on,
        logged_off=logged_off
    )
