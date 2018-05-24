import time


class PcAction(object):

    def __init__(self):
        self.status_code = 'error'

    def change_status_code(self, incoming_status):
        self.status_code = incoming_status
        print(self.status_code)

    def get_status_code(self):
        return self.status_code

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

