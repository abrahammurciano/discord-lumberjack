# discord-lumberjack

A Python logging handler which sends its logs to a Discord Channel or Webhook.

## Documentation

You can find the documentation [here](https://abrahammurciano.github.io/discord-lumberjack/discord_lumberjack/).

## Installation

To install this python module, run the following command

```
$ pip install discord-lumberjack
```

<!-- handlers_start -->

## Handlers

This python module provides several logging handlers (located in the `discord_lumberjack.handlers` module) which will send the logs it recieves to a Discord webhook, server channel, or DM channel.

The available handlers are:

-   `DiscordChannelHandler` - Uses a bot token and a channel ID to send logs to the given channel from the given bot.
-   `DiscordDMHandler` - Uses a bot token and a user ID to send logs to the given user from the given bot.
-   `DiscordWebhookHandler` - Uses a webhook URL to send the logs to.
-   `DiscordHandler` - This is the base class for the other three. You probably don't want to use this unless you're creating your own fancy handler.

<!-- handlers_end -->
<!-- message_creators_start -->

## Message Creators

In order to send nice looking messages, there are a few message creators available (located in the `discord_lumberjack.message_creators` module). These are responsible for converting a `logging.LogRecord` into a message structure that will be sent to Discord's API.

The message creators provided currently will split extremely long messages into several in order to fit within Discord's message limits. If you decide to create your own one, keep that in mind too.

The available message creators are:

-   `BasicMessageCreator` - This is a simple message creator which will use the handler's set formatter to send the message as plain text. By default, the message will be formatted in monospace, but this can be disabled via the constructor.
-   `EmbedMessageCreator` - This message creator will create a fancy-looking embed message from the log record. It will ignore the handler's formatter.

<!-- message_creators_end -->

## Usage

The easiest way to get started is to create a webhook and use that, but if you're using this to log a Discord bot, you can use it's token directly, without needing to create webhooks.

### Import

First, you should import the handlers you want to use. For this example, we'll assume we have a Discord bot and we'd like to use it to log every message to a channel and also to send errors to a DM.

We'll be using the `DiscordChannelHandler` to send all messages of level `INFO` and above to the channel and `DiscordDMHandler` to send messages of level `ERROR` and above to a DM.

```py
from discord_lumberjack.handlers import DiscordChannelHandler, DiscordDMHandler
```

### Basic Setup

You should really read the [documentation for the `logging` module](https://docs.python.org/3/howto/logging.html#logging-basic-tutorial) to learn how to set up your logging, but here's a quick snippet to get you started.

```py
import logging
logging.basicConfig(
	level=logging.INFO,
	handlers=[
		DiscordChannelHandler(token=my_bot_token, channel_id=my_channel_id),
		DiscordDMHandler(token=my_bot_token, user_id=my_user_id, level=logging.ERROR),
	]
)
```

Once you've set up your logging, you can start logging messages like this:

```py
logging.info("This is an informative message that will be sent to the channel.")
logging.error("This is an error, so it will also be sent to the DM.")
```
