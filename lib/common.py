#! /usr/bin/env python3

""" Common utils for paterica """

import logging
from dataclasses import dataclass, field
import telegram


@dataclass
class InitBotConfig:
    """ Init bot specific conf """
    target: int
    interval: int


@dataclass
class PatericaConfig:
    """ General bot config """
    name: str
    token: str
    init_bot: InitBotConfig
    bot: telegram.Bot
    log: logging.Logger = field(default_factory=logging.getLogger)


def yaml_to_config(yaml: dict) -> PatericaConfig:
    """ Convert yaml to config """
    return PatericaConfig(
        name=yaml["name"],
        token=yaml["authToken"],
        init_bot=InitBotConfig(
            target=int(yaml["init"]["target"]),
            interval=int(yaml["init"]["intervalSeconds"]),
        ),
        bot=telegram.Bot(yaml["authToken"]),
    )
