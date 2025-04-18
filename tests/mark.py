def slow(cls):
    return cls


def filterwarnings(msg):
    def func(cls):
        return cls
