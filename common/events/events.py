class Event(object):
    def __init__(self, info):
        self.info = info


class SetPathEvent(Event):
    def __init__(self, info, *args, **kwargs):
        super().__init__(info)


class EndTaskEvent(Event):
    def __init__(self, info):
        super().__init__(info)
