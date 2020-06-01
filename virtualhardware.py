class dummy_adafruit_dht:
    def __init__(self):
        pass

class dummy_GPIO:
    def __init__(self):
        OUT = 'out'
        BCM = 'bcm'
    def setwarnings(*args, **kwargs):
        print('setwarnings args {} kwargs {}'.format(args, kwargs))
    def setup(*args, **kwargs):
        print('setup args {} kwargs {}'.format(args, kwargs))
    def output(*args, **kwargs):
        print('output args {} kwargs {}'.format(args, kwargs))
    def setmode(*args, **kwargs):
        print('setmode args {} kwargs {}'.format(args, kwargs))

class dummy_W1ThermSensor:
    def __init__(self):
        pass




