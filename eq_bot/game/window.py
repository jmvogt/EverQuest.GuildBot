import time
import win32gui
from pynput.keyboard import Key
from dataclasses import dataclass
from game.entities.player import CurrentPlayer

from game.logging.log_reader import EverQuestLogReader

from utils.input import send_text, send_multiple_keys, send_key

# TODO: Move to configuration file
EVERQUEST_ROOT_FOLDER='C:\\Program Files (x86)\\Steam\\steamapps\\common\\Everquest F2P'


@dataclass
class EverQuestWindow:
    player: CurrentPlayer

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
        self.activate()
        return self.send_chat_message(f"/outputfile guild {outputfile}")

    def get_player_log_reader(self):
        return EverQuestLogReader(f'{EVERQUEST_ROOT_FOLDER}\\Logs', self.player)
