#! /usr/bin/env python3

"""
Init bot. Makes sure to spam connectivity data if no user is logged in.
"""

import asyncio
import logging
import pprint
import sys
from time import sleep
from typing import Callable

import psutil
import telegram
import ruamel.yaml

import lib.common as c


def get_logins() -> list[str]:
    """ Get a list of logged in linux users. """
    return list((u.name for u in psutil.users()))


async def send_message(
    bot: telegram.Bot,
    chat_id: int,
    message: str,
) -> None:
    """ Send a message to a chat. """
    async with bot:
        await bot.send_message(chat_id, message)


def should_notify(
    users: list[str],
    count: int,
) -> bool:
    """ Check if we should notify. """

    if len(users) < count:
        return False
    return True


def main(
    bot: telegram.Bot,
    conf: c.InitBotConfig,
    _log: logging.Logger,
    msg_func: Callable[[], str],
) -> None:
    """ Main function. """

    while True:
        users = get_logins()
        if should_notify(users, 0):
            _log.info(f"Sending notification msg to {conf.target}")
            asyncio.run(send_message(bot, conf.target, msg_func()))
        sleep(conf.interval)


if __name__ == "__main__":
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        config = c.yaml_to_config(ruamel.yaml.YAML().load(f))
    main(
        config.bot, config.init_bot, config.log,
        lambda: "My interfaces:\n" + pprint.pformat(
            {k: [card.address for card in v]
             for k, v in psutil.net_if_addrs().items()}
        )
    )
