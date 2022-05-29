from pathlib import Path

from common.observer import Observable


class Model(Observable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    m = Model()
    test_path = Path.home().resolve()
    m.collect_metrics(str(test_path), [str(Path('.').resolve())], 'test.json')
