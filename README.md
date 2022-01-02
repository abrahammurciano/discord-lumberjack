# py-logging-discord
A Python logging handler which sends its logs to a Discord Channel

# Installation

To install this python module, run the following command

```
$ pip install py-logging-discord
```

# Usage

This python module provides a logging handler which will send the logs it recieves to a discord channel or DM you specify.

### Import

First, you should import the handler.

```py
from py_logging_discord import DiscordLogHandler
```

### Construction

You should then construct the handler. Here are all the available options you may pass to the handler's constructor.

- **token** *str* - A bot's token, provided by Discord, used to send the log messages from that bot.
- **channel_id** *int* - The ID of a discord channel or DM which the bot is allowed to send messages to.
