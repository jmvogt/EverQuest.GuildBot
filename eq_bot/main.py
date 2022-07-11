import time
from datetime import timedelta
from game.window import EverQuestWindow
from game.guild.dump_manager import GuildDumpManager
from utils.input import has_recent_input, get_timedelta_since_input
from game.entities.player import CurrentPlayer
from game.logging.entities.log_message import LogMessageType

# TODO: Move to configuration file
TICK_LENGTH = 1
EQ_PLAYER = 'Maeby'
EQ_SERVER = 'Mischief'

current_player = CurrentPlayer(name=EQ_PLAYER, server=EQ_SERVER)

window = EverQuestWindow(current_player)
player_log_reader = window.get_player_log_reader()
# TODO: Enable based on configuration
# player_log_reader.cycle_player_log()

guild_dump_manager = GuildDumpManager(window)

player_log_reader.observe_messages(LogMessageType.TELL_RECEIVE, lambda message: message.print())

while(True):
    if has_recent_input():
        time.sleep(1)
        continue
    player_log_reader.process_new_messages()
    # TODO: Enabled based on configuration
    guild_dump_manager.handle_tick()
    time.sleep(TICK_LENGTH)
