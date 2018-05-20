import mqtt_remote_method_calls as com
import time
import controller

class PCDelegate(object):
    def __init__(self):
        self.red1 = 'I smell blood!'
        self.blue1 = 'I smell my water bowl'
        self.black1 = 'I smell black paint'

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    def red(self):
        print(self.red1)

    def blue(self):
        print(self.blue1)

    def black(self):
        print(self.black1)