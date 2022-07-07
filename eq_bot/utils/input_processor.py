import random
from time import sleep
from pynput.keyboard import Key, Controller

# TODO: Move to configuration file
MIN_PRESS_DELAY = .100
MAX_PRESS_DELAY = .225

# TODO: Send commands to process in background rather than sending keypresses to current screen
_keyboard = Controller()

def _sleep(modifier = 1.0):
    sleep(random.uniform(MIN_PRESS_DELAY * modifier, MAX_PRESS_DELAY * modifier))

def send_key(key):
    if type(key) == str and key.isupper():
        send_multiple_keys([Key.shift, key.lower()])
    else:
        _keyboard.press(key)
        _keyboard.release(key)
        _sleep()

def send_text(text):
    for character in text:
        if character == " ":
            send_key(Key.space)
        else:
            send_key(character)

def send_multiple_keys(keys):
    for key in keys:
        _keyboard.press(key)
        _sleep(.33)

    for key in keys:
        _keyboard.release(key)
        _sleep(.33)
