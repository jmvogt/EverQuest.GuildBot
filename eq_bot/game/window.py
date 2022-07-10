import time
import win32gui
from pynput.keyboard import Key
from dataclasses import dataclass
from os.path import exists
from utils.file import move_file
from datetime import datetime

from utils.input import send_text, send_multiple_keys, send_key

# TODO: Move to configuration file
EVERQUEST_ROOT_FOLDER='C:\\Program Files (x86)\\Steam\\steamapps\\common\\Everquest F2P'
PLAYER_LOG_TIMESTAMP_FORMAT='%Y%m%d-%H%M%S'

@dataclass
class EverQuestWindow:
    def _lookup(self):
        return win32gui.FindWindow(None, "EverQuest")

    def activate(self):
        win32gui.SetForegroundWindow(self._lookup())
        time.sleep(.5)

    def clear_chat(self):
        send_multiple_keys([Key.shift, Key.delete])
        send_key(Key.enter)

    def send_chat_message(self, message):
        self.clear_chat()
        send_text(message)
        send_key(Key.enter)

    def guild_dump(self, outputfile):
        return self.send_chat_message(f"/outputfile guild {outputfile}")

    def _get_log_folder(self):
        return f'{EVERQUEST_ROOT_FOLDER}\\Logs'

    def _get_log_filename(self, player, server):
        return f'eqlog_{player}_{server.lower()}'

    def get_player_log(self, player, server, filename=None):
        if not filename:
            filename = self._get_log_filename(player, server)
        return f'{self._get_log_folder()}\\{filename}.txt'

    def cycle_player_log(self, player, server):
        current_player_log = self.get_player_log(player, server)
        if not exists(current_player_log):
            return
        new_filename = f'{self._get_log_filename(server, player)}-{datetime.now().strftime(PLAYER_LOG_TIMESTAMP_FORMAT)}'
        move_file(current_player_log, self.get_player_log(player, server, new_filename))
