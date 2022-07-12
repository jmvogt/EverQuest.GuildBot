import random
from datetime import datetime, timedelta
from dataclasses import dataclass
from game.window import EverQuestWindow, EVERQUEST_ROOT_FOLDER
from game.guild.dump_parser import parse_dump_file
from game.guild.dump_analyzer import build_differential
from game.guild.formatter.discord_dump_formatter import DiscordDumpFormatter
from integrations.discord import send_discord_message
from utils.file import move_file, make_directory, get_files_from_directory
from utils.config import get_config
from utils.array import contains

# TODO: Move to configuration file
DUMP_EXTENSION='.dump'
DUMP_OUTPUT_FOLDER='output\\dumps\\guild'
DUMP_TIME_FORMAT='%Y%m%d-%H%M%S'
FREQUENCY_MIN=get_config('guild_tracking.interval_min', 300)
FREQUENCY_MAX=get_config('guild_tracking.interval_max', 600)
OUTPUT_TO_DISCORD=get_config('guild_tracking.output_to_discord')

class GuildTracker:
    def __init__(self, eq_window: EverQuestWindow):
        make_directory(DUMP_OUTPUT_FOLDER)
        self._eq_window = eq_window
        self._last_dump = self._lookup_most_recent_dump()
        self._discord_formatter = DiscordDumpFormatter()

    def _get_safe_guild_name(self):
        return self._eq_window.player.guild.replace(' ', '-')

    def _lookup_most_recent_dump(self):
        previous_dump_files = get_files_from_directory(DUMP_OUTPUT_FOLDER, DUMP_EXTENSION)
        previous_dumps = []
        for dump_file in previous_dump_files:
            dump_time = datetime.strptime(dump_file, f"{self._get_safe_guild_name()}-Dump-{DUMP_TIME_FORMAT}{DUMP_EXTENSION}")
            previous_dumps.append(parse_dump_file(dump_time, f"{DUMP_OUTPUT_FOLDER}\{dump_file}"))
        previous_dumps.sort(key=lambda x: x.taken_at, reverse=True)
        return None if not previous_dumps else previous_dumps[0]

    def _create_dump(self):
        dump_time = datetime.now()
        dump_time_str = dump_time.strftime(DUMP_TIME_FORMAT)
        dump_filename = f"{self._get_safe_guild_name()}-Dump-{dump_time_str}"
        self._eq_window.guild_dump(dump_filename)
        dump_filepath = f"{EVERQUEST_ROOT_FOLDER}\{dump_filename}.txt"
        
        new_dump = parse_dump_file(dump_time, dump_filepath)
        new_dump.print()

        if self._last_dump:
            dump_differential = build_differential(self._last_dump, new_dump)
            dump_differential.print()

            if dump_differential.has_differences and OUTPUT_TO_DISCORD:
                send_discord_message(self._discord_formatter.build_output(dump_differential))

        self._last_dump = new_dump

        # Backup file in local output for future parsing
        move_file(dump_filepath, f"{DUMP_OUTPUT_FOLDER}\{dump_filename}{DUMP_EXTENSION}")

    def update_status(self):
        if not self._last_dump or datetime.now() + timedelta(seconds=-random.randint(FREQUENCY_MIN, FREQUENCY_MAX)) > self._last_dump.taken_at:
            self._create_dump()

    def is_a_member(self, name):
        if not self._last_dump:
            raise ValueError("Last dump has not yet been taken.")
        
        # TODO: Change self.members structure so that we can more easily lookup by name..
        return contains(self._last_dump.members, lambda member: member.name.lower() == name.lower())
