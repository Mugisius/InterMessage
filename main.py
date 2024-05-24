import asyncio
import argparse
import yaml

from translator import translate
from TelegramBot import TelegramBot
from VkBot import VkBot
from DiscordBot import DiscordBot
from Logger import Logger

def get_bot(messenger, parameters):

    match messenger:
        case "telegram":
            return TelegramBot(parameters)
        case "vk":
            return VkBot(parameters)
        case "discord":
            return DiscordBot(parameters)
        case "logger":
            return Logger(parameters)


#узел сети InterMessage, содержит объект бота и очереди входных сообщений и выходных сообщений
class IMNode():

    def __init__(self, messenger, parameters):
        self.incoming = asyncio.Queue()
        self.outcoming = asyncio.Queue()

        self.bot = get_bot(messenger, parameters)
        self.bot.set_queues(self.incoming, self.outcoming)

        self.loop = self.bot.start()
        self.messenger = messenger

    def connect_to_other_nodes(self, all_nodes):
        self.all_nodes = all_nodes

    async def send_to_node(self, message, node):
        await node.incoming.put(message)

    async def send_to_other_nodes(self, message):
        for node in self.all_nodes:
            if node != self:
                message.sourse = self.messenger
                await self.send_to_node(translate(message, self.messenger, node.messenger), node)

    async def run_send(self):
        while True:
            message_out = await self.outcoming.get()
            await self.send_to_other_nodes(message_out)

    async def run_rcv(self):
        while True:
            message_in = await self.incoming.get()
            await self.bot.send(message_in)

async def main(nodes, loops):
    cycles = []
    for node in nodes:
        cycles.append(node.run_send())
        cycles.append(node.run_rcv())

    await asyncio.gather(*cycles, *loops)

def get_args():
    parser = argparse.ArgumentParser(description="Приложение InterMessage для объединения чатов в разных мессенджерах")
    parser.add_argument("conf_path", help="Путь к файлу с конфигуацией ботов в мессенджерах", type=str)

    args = parser.parse_args()
    return args

def validate(conf):
    #TODO Добавить валидацию конфигурации согласно спроектированному синтаксису
    pass

def create_nodes_by_conf(conf_path):
    with open(conf_path) as conf_file:
        conf = yaml.load(conf_file, Loader=yaml.loader.SafeLoader)
        validate(conf)

        nodes = []
        loops = []
        for messenger in conf.values():
            nodes.append(IMNode(messenger['name'], messenger['parameters']))
            loops.append(nodes[-1].loop)
        
        return nodes, loops
    
def connect_nodes(nodes):
    for node in nodes:
        node.connect_to_other_nodes(nodes)

if __name__ == "__main__":
    # args = get_args()

    nodes, loops = create_nodes_by_conf('ttt.yaml')#args.conf_path)
    connect_nodes(nodes)
    asyncio.run(main(nodes, loops))


