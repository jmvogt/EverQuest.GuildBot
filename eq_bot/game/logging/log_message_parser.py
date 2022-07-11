import shlex
from datetime import datetime
from game.logging.entities.log_message import LogMessage, LogMessageType

PLAYER_MESSAGES = ['tells', 'says', 'shouts', 'auctions', 'channel']

def _parse_timestamp(input):
    return datetime.strptime(input, "[%a %b %d %H:%M:%S %Y]")

def _parse_message_type(full_message, message_split):
    message_without_name = ' '.join(message_split[2:])
    if message_split[1] == 'tells':
        # e.g. General:3
        if len(message_split[2].split(':')) > 1:
            return LogMessageType.CHANNEL
        elif message_split[2] == 'you,':
            return LogMessageType.TELL_RECEIVE
        elif message_split[2] == 'the':
            if message_split[3] == 'group,':
                return LogMessageType.GROUP
            elif message_split[3] == 'guild,':
                return LogMessageType.GUILD
    elif message_split[1] == 'says':
        if message_without_name.startswith('out of character,'):
            return LogMessageType.OUT_OF_CHARACTER
    elif message_split[1] == 'auctions,':
        return LogMessageType.AUCTION
    elif message_split[1] == 'shouts,':
        return LogMessageType.SHOUT
    elif message_split[1] == 'says,':
        if len(message_split) == 3:
            return LogMessageType.SAY
    elif message_without_name.startswith('You tell'):
        return LogMessageType.TELL_SEND
    return LogMessageType.UNKNOWN

def _parse_message_to(full_message, message_split, message_type):
    if message_type not in [LogMessageType.CHANNEL, LogMessageType.TELL_RECEIVE, LogMessageType.TELL_SEND]:
        return
    
    if message_type == LogMessageType.CHANNEL:
        return message_split[2].split(':')[0]
    elif message_type == LogMessageType.TELL_RECEIVE or message_type == LogMessageType.TELL_SEND:
        return message_split[2].rstrip(',').capitalize()
    # TODO: Log warning

def create_log_message(raw_text):
    full_message = raw_text[27:].rstrip('\n')
    message_split = shlex.split(full_message)
    message_type = _parse_message_type(full_message, message_split)
    is_player_message = message_type != LogMessageType.UNKNOWN

    return LogMessage(
        timestamp = _parse_timestamp(raw_text[0:26]),
        from_player = message_split[0] if is_player_message else None,
        to = _parse_message_to(full_message, message_split, message_type),
        full_message = full_message,
        message_type = message_type)
