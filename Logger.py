from BotBase import BotBase

class Logger(BotBase):
    def __init__(self, parameters):
        log_file = open(parameters["logPath"], "w")
        self.log_file = log_file
        async def loop():
            pass
        self.loop = loop
        print("Created Logger")
    
    def base_message_handler(self, msg):
        pass

    def send(self, msg):
        self.log_file.write(msg)
    