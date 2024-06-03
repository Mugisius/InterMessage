"""Programm for resending messages between different chats."""
import asyncio
import argparse
import yaml
import os
import gettext

from .Bots.TelegramBot import TelegramBot
from .Bots.VkBot import VkBot
from .Bots.DiscordBot import DiscordBot
from .Bots.Logger import Logger

import logging

logging.basicConfig(level=logging.ERROR)


def get_bot(messenger, parameters):
    """
    Get bot object by its string name.

    :param messenger: string name of bot type
    :param parameters: parameters of the bot
    """
    match messenger:
        case "telegram":
            return TelegramBot(parameters)
        case "vk":
            return VkBot(parameters)
        case "discord":
            return DiscordBot(parameters)
        case "logger":
            return Logger(parameters)


class IMNode():
    """
    Node of InterMessage network.

    One node of InterMessage network
    It contains bot object, queues of incoming and outcoming messages
    """

    def __init__(self, messenger, parameters):
        """Set up queues, bot object and async bot loop.

        :param messenger: string name of bot type
        :param parameters: parameters of the bot
        """
        self.incoming = asyncio.Queue()
        self.outcoming = asyncio.Queue()

        self.bot = get_bot(messenger, parameters)
        self.bot.set_queues(self.incoming, self.outcoming)

        self.loop = self.bot.start()
        self.messenger = messenger

    def connect_to_other_nodes(self, all_nodes):
        """
        Set up a list of all IMNodes.

        :param all_nodes: list of all IMNodes
        """
        self.all_nodes = all_nodes

    async def send_to_node(self, message, node):
        """
        Send message to IMNode.

        :param message: message to send
        :param node: target IMNode
        """
        await node.incoming.put(message)

    async def send_to_other_nodes(self, message):
        """
        Send message to all other IMNodes.

        :param message: message to send
        """
        for node in self.all_nodes:
            if node != self:
                await self.send_to_node(message, node)

    async def run_send(self):
        """Coroutine for sending outcoming message to all other IMNodes."""
        while True:
            message_out = await self.outcoming.get()
            await self.send_to_other_nodes(message_out)

    async def run_rcv(self):
        """Coroutine for sending incoming message to bot."""
        while True:
            message_in = await self.incoming.get()
            await self.bot.send(message_in)


async def gather(nodes, loops):
    """
    Start async loop for bots and message handlers.

    :param nodes: list of all IMNodes
    :param loops: loops of all bots
    """
    cycles = []
    for node in nodes:
        cycles.append(node.run_send())
        cycles.append(node.run_rcv())

    await asyncio.gather(*cycles, *loops)


def get_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description=_("InterMessage application for connecting chats in different messengers")
    )
    parser.add_argument(
        "conf_path",
        help=_("The path to the file with the configuration of bots in messengers"),
        type=str
    )
    parser.add_argument(
        "--lang",
        help=_("The language of the bot's messages"),
        type=str
    )

    args = parser.parse_args()
    return args


def validate(conf):
    """
    Validate configuration from .yaml file.

    :param conf: dict loaded from .yaml file
    """
    try:
        if not conf:
            raise KeyError

        for messenger in conf.values():
            match messenger["name"]:
                case "telegram" | "vk" | "discord":
                    messenger["parameters"]["token"]
                    messenger["parameters"]["channel"]
                case "logger":
                    messenger["parameters"]["logPath"]
                case _:
                    raise KeyError
    except KeyError:
        return False

    return True


def create_nodes_by_conf(conf_path):
    """
    Create IMNodes by configuration file.

    :param conf_path: path to configuration .yaml file
    """
    with open(conf_path) as conf_file:
        conf = yaml.load(conf_file, Loader=yaml.loader.SafeLoader)

        if not validate(conf):
            print(_("Invalid configuration file"))
            exit(0)

        nodes = []
        loops = []
        for messenger in conf.values():
            nodes.append(IMNode(messenger['name'], messenger['parameters']))
            loops.append(nodes[-1].loop)

        return nodes, loops


def connect_nodes(nodes):
    """
    Connect IMNodes.

    :param nodes: list of all IMNodes
    """
    for node in nodes:
        node.connect_to_other_nodes(nodes)


def main():
    """Call main application."""
    translation = gettext.translation("IM", os.path.dirname(__file__), fallback=True)
    translation.install()

    args = get_args()

    logging.basicConfig(level=logging.ERROR)

    if args.lang:
        langs = [args.lang]
    else:
        langs = None

    translation = gettext.translation("IM", os.path.dirname(__file__), langs, fallback=True)
    translation.install()

    nodes, loops = create_nodes_by_conf(args.conf_path)
    connect_nodes(nodes)
    try:
        asyncio.run(gather(nodes, loops))
    except KeyboardInterrupt:
        print(_("Received exit, exiting"))
