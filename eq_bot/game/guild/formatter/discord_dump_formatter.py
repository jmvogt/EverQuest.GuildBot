from game.guild.entities.guild_dump_differential import GuildDumpDifferential
from game.guild.dump_analyzer import DAYS_UNTIL_OFF_DUTY

class DiscordDumpFormatter:
    def build_output(self, dump_differential: GuildDumpDifferential) -> str:
        minutes = dump_differential.delta_time.total_seconds() / 60
        hours = minutes / 60
        minutes = int(minutes % 60)
        days = int(hours / 24)
        hours = int(hours % 24)

        discord_message = f"__**Guild Status Report**__\n"
        discord_message += f"_{days} days, {hours} hours, and {minutes} minutes since last report_\n\n"

        if len(dump_differential.new_members) > 0:
            discord_message += f"**Joined**\n"
            discord_message += f"```diff\n"
            for member in dump_differential.new_members:
                discord_message += f"+ {member.name} - {member.level} {member.class_type} {'(Alt)' if member.is_alt else ''}\n"
            discord_message += "```\n"

        if len(dump_differential.offduty_members) > 0:
            discord_message += f"**Inactive ({DAYS_UNTIL_OFF_DUTY} days)**\n"
            discord_message += f"```fix\n"
            for member in dump_differential.offduty_members:
                discord_message += f"- {member.name} - {member.level} {member.class_type} {'(Alt)' if member.is_alt else ''}\n"
            discord_message += "```\n"

        if len(dump_differential.left_members) > 0:
            discord_message += f"**Left**\n"
            discord_message += f"```diff\n"
            for member in dump_differential.left_members:
                discord_message += f"- {member.name} - {member.level} {member.class_type} {'(Alt)' if member.is_alt else ''}\n"
            discord_message += "```\n"

        return discord_message + "\n"
