import random
from datetime import datetime, timedelta
from dataclasses import dataclass
from game.window import EverQuestWindow, EVERQUEST_ROOT_FOLDER
from game.guild.dump_parser import parse_dump_file
from game.guild.dump_analyzer import build_differential
from integrations.discord import send_discord_message
from utils.file import move_file, make_directory, get_files_from_directory
from utils.config import get_config

# TODO: Move to configuration file
GUILD_DUMP_FILE_PREFIX='RMPD-Guild-Dump'
DUMP_EXTENSION='.dump'
DUMP_OUTPUT_FOLDER='output\\dumps\\guild'
DUMP_TIME_FORMAT='%Y%m%d-%H%M%S'
FREQUENCY_MIN=get_config('guild_dumps.interval_min')
FREQUENCY_MAX=get_config('guild_dumps.interval_max')


class GuildDumpManager:
    def __init__(self, eq_window: EverQuestWindow):
        make_directory(DUMP_OUTPUT_FOLDER)
        self._eq_window = eq_window
        self._last_dump = self._lookup_most_recent_dump()

    def _lookup_most_recent_dump(self):
        previous_dump_files = get_files_from_directory(DUMP_OUTPUT_FOLDER, DUMP_EXTENSION)
        previous_dumps = []
        for dump_file in previous_dump_files:
            dump_time = datetime.strptime(dump_file, f"{GUILD_DUMP_FILE_PREFIX}-{DUMP_TIME_FORMAT}{DUMP_EXTENSION}")
            previous_dumps.append(parse_dump_file(dump_time, f"{DUMP_OUTPUT_FOLDER}\{dump_file}"))
        previous_dumps.sort(key=lambda x: x.taken_at, reverse=True)
        return None if not previous_dumps else previous_dumps[0]

    def _create_dump(self):
        dump_time = datetime.now()
        dump_time_str = dump_time.strftime(DUMP_TIME_FORMAT)
        dump_filename = f"{GUILD_DUMP_FILE_PREFIX}-{dump_time_str}"
        self._eq_window.guild_dump(dump_filename)
        output_filename = f"{DUMP_OUTPUT_FOLDER}\{dump_filename}{DUMP_EXTENSION}"
        move_file(f"{EVERQUEST_ROOT_FOLDER}\{dump_filename}.txt", output_filename)
        
        new_dump = parse_dump_file(dump_time, output_filename)
        new_dump.print()

        if self._last_dump:
            dump_differential = build_differential(self._last_dump, new_dump)
            dump_differential.print()

            if dump_differential.has_differences:
                # TODO: Move to a formatter class
                time_format = "%D %H:%M:%S"
                discord_message = f"**Guild Status Report:** {new_dump.taken_at.strftime(time_format)}\n" +\
                    f"**Previous Report:** {self._last_dump.taken_at.strftime(time_format)}\n>>> "
                
                if len(dump_differential.new_members) > 0:
                    discord_message += f"**Joined:**\n"
                    for member in dump_differential.new_members:
                        discord_message += f"{member.name} - {member.level} {member.class_type} {'(Alt)' if member.is_alt else ''}\n"
                    discord_message += "\n"
                
                if len(dump_differential.left_members) > 0:
                    discord_message += f"**Deguilded:**\n"
                    for member in dump_differential.left_members:
                        discord_message += f"{member.name} - {member.level} {member.class_type} {'(Alt)' if member.is_alt else ''}\n"
                    discord_message += "\n"

                if len(dump_differential.left_members) > 0:
                    discord_message += f"**Off Duty:**\n"
                    for member in dump_differential.offduty_members:
                        discord_message += f"{member.name} - {member.level} {member.class_type} {'(Alt)' if member.is_alt else ''}\n"
                    discord_message += "\n"

                if len(dump_differential.logged_on) > 0:
                    discord_message += f"**Logged In:**\n"
                    for member in dump_differential.logged_on:
                        discord_message += f"{member.name} - {member.level} {member.class_type} {'(Alt) ' if member.is_alt else ''}- {member.zone}\n"
                    discord_message += "\n"

                if len(dump_differential.logged_off) > 0:
                    discord_message += f"**Logged Off:**\n"
                    for member in dump_differential.logged_off:
                        discord_message += f"{member.name} - {member.level} {member.class_type} {'(Alt)' if member.is_alt else ''}\n"
                    discord_message += "\n"

                send_discord_message(discord_message + "\n")
        
        self._last_dump = new_dump

    def handle_tick(self):
        if not self._last_dump or datetime.now() + timedelta(seconds=-random.randint(FREQUENCY_MIN, FREQUENCY_MAX)) > self._last_dump.taken_at:
            self._create_dump()
