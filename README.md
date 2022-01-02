# py-logging-discord
A Python logging handler which sends its logs to a Discord Channel

# Installation

To install this python module, run the following command

```
$ pip install py-logging-discord
```

# Usage

This python module provides a logging handler which will send the logs it recieves to a discord channel, and another which sends them to a DM. In order to use this module, you must first create a Discord bot. This can be done on the [Discord Developer Portal](https://discord.com/developers/applications).

### Import

First, you should import the handler. You can import `DiscordLogHandler` to log to a channel, or `DiscordDmLogHandler` to log to a DM, or both.

```py
from py_logging_discord import DiscordLogHandler, DiscordDmLogHandler
```

### Construction

You should then construct the handler. Here are all the available arguments you may pass to `DiscordLogHandler`'s constructor.

- **token** *str* - A bot's token, provided by Discord, used to send the log messages from that bot.
- **channel_id** *int* - The ID of a discord channel which the bot is allowed to send messages to. Logs will be sent to this channel.
- **level** *int, optional* - The minimum log level that this handler should handler. You probably want to use one of these values: `logging.NOTSET`, `logging.DEBUG`, `logging.INFO`, `logging.WARNING`, `logging.ERROR`, or `logging.CRITICAL`. The default value is `logging.NOTSET`. [Read more about log levels.](https://docs.python.org/3/library/logging.html#logging-levels)

Here are the parameters available to `DiscordDmLogHandler`.

- **token** *str* - Same as for `DiscordLogHandler.
- **user_id** *int* - The ID of a user whom the bot is allowed to send messages to. Logs will be sent to this user.
- **level** *int, optional* - Same as for `DiscordLogHandler`.


