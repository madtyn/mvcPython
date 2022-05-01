class MockController(object):
    def __init__(self):
        pass

    @staticmethod
    def get_combo_options():
        return 'fake1', 'fake2', 'fake3', 'fake4'

    def collect_metrics(self, *args, **kwargs):
        pass