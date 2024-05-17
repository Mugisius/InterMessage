import asyncio
import argparse
import yaml

from translator import translate
import TelegramBot
import VkBot
import DiscordBot

def get_bot(messenger, parameters):

    match messenger:
        case "telegram":
            return TelegramBot(parameters)
        case "vk":
            return VkBot(parameters)
        case "discord":
            return DiscordBot(parameters)


#узел сети InterMessage, содержит объект бота и очереди входных сообщений и выходных сообщений
class IMNode():

    def __init__(self, messenger, parameters):
        self.incoming = asyncio.Queue()
        self.outcoming = asyncio.Queue()

        self.bot = get_bot(messenger, parameters)
        self.bot.set_queues(self.incoming, self.outcoming)

        self.messenger = messenger

    def connect_to_other_nodes(self, all_nodes):
        self.all_nodes = all_nodes

    def send_to_node(self, message, node):
        node.incoming.put(message)

    def send_to_other_nodes(self, message):
        for node in self.all_nodes:
            if node != self:
                self.send_to_node(translate(message, self.messenger, node.messenger), node)

    async def run_send(self):
        while True:
            message_out = await self.outcoming.get()
            self.send_to_other_nodes(message_out)

    async def run_rcv(self):
        while True:
            message_in = await self.incoming.get()
            self.bot.send(message_in)

async def main(nodes):
    cycles = []
    for node in nodes:
        cycles.append(node.run_send())
        cycles.append(node.run_rcv())

    await asyncio.gather(*cycles)

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
        conf = yaml.load(conf_file)
        validate(conf)

        nodes = []
        for messenger in conf:
            nodes.append(IMNode(messenger['name'], messenger['parameters']))
        
        return nodes
    
def connect_nodes(nodes):
    for node in nodes:
        node.connect_to_other_nodes(nodes)

if __name__ == "__main__":
    args = get_args()

    nodes = create_nodes_by_conf(args.conf_path)
    connect_nodes(nodes)
    asyncio.run(main(nodes))


