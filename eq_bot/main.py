import time
from datetime import timedelta
from game.window import EverQuestWindow
from game.guild_dump.manager import GuildDumpManager
from utils.input import has_recent_input, get_timedelta_since_input

# TODO: Move to configuration file
TICK_LENGTH = 60
EQ_PLAYER = 'Fanoen'
EQ_SERVER = 'Mischief'

window = EverQuestWindow()
window.cycle_player_log(EQ_PLAYER, EQ_SERVER)

guild_dump_manager = GuildDumpManager(window)

while(True):
    if has_recent_input():
        time.sleep(1)
        continue
    window.activate()
    guild_dump_manager.handle_tick()
    time.sleep(TICK_LENGTH)
