import asyncio

#узел сети InterMessage, содержит объект бота и очереди входных сообщений и выходных сообщений
class IMNode():

    def __init__(self, name, parameters):
        self.incoming = []
        self.outgoing = []

        self.bot = import_bot(name)
        self.bot.set_parameters(parameters)
        self.bot.set_queues(self.incoming, self.outgoing)

    

    async def run():
        message_out = await coroutine1
        send_to_other_nodes(message_out)

    async def run2():
        message_in = await coroutine2
        bot.send(message_in)








# получить конфигурацию
cnf = load_config(argv[1])

#по конфигурации построить сеть, соединение каждый с каждым
net = get_bots_from_cnf(cnf)

cycles = []
for nodes in net:
    cycles.append(bot.run)

asyncio.gather(cycles)
asyncio.run()

