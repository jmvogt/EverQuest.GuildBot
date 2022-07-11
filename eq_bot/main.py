import time
from datetime import timedelta
from game.window import EverQuestWindow
from game.guild.dump_manager import GuildDumpManager
from utils.input import has_recent_input, get_timedelta_since_input
from game.entities.player import CurrentPlayer
from game.logging.entities.log_message import LogMessageType
from utils.config import get_config

EQ_PLAYER = get_config('player')
EQ_SERVER = get_config('server')
TICK_LENGTH = 1

current_player = CurrentPlayer(name=EQ_PLAYER, server=EQ_SERVER)

window = EverQuestWindow(current_player)
player_log_reader = window.get_player_log_reader()

if get_config('log_parsing.cycle_on_start'):
    player_log_reader.cycle_player_log()

guild_dump_manager = GuildDumpManager(window)

player_log_reader.observe_messages(LogMessageType.TELL_RECEIVE, lambda message: message.print())

while(True):
    if not has_recent_input():
        if get_config('log_parsing.enabled'):
            player_log_reader.process_new_messages()
        if get_config('guld_dumps.enabled'):
            guild_dump_manager.handle_tick()
    time.sleep(TICK_LENGTH)
