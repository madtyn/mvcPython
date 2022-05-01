import os
from pathlib import Path

ROOT_PATH = (Path(os.path.dirname(__file__)) / '..').resolve()
ASSETS_PATH = ROOT_PATH / 'assets'

if __name__ == '__main__':
    p = Path(__file__)
    print(p)
    print(__file__)
