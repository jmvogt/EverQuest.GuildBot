import time
from game.window import EverQuestWindow
from game.guild_dump.manager import GuildDumpManager

# TODO: Move to configuration file
TICK_LENGTH = 60

window = EverQuestWindow()
guild_dump_manager = GuildDumpManager(window)

while(True):
    window.activate()
    guild_dump_manager.handle_tick()
    time.sleep(TICK_LENGTH)
