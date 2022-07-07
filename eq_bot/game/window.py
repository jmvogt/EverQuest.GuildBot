import time
import win32gui
from pynput.keyboard import Key
from dataclasses import dataclass

from utils.input_processor import send_text, send_multiple_keys, send_key

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
