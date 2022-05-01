import tkinter as tk
from common.utils import ASSETS_PATH


class IconProvider(object):
    OPEN_FOLDER = 'open_folder'
    SAVE_DISK = 'save_disk'
    GARBAGE_BIN = 'garbage_bin'
    METRICS = 'metrics'
    icons = {}

    @staticmethod
    def get(icon_key):
        if icon_key in IconProvider.icons:
            new_icon = IconProvider.icons.get(icon_key)
        else:
            new_icon = tk.PhotoImage(file=str(ASSETS_PATH / f'{icon_key}.png'))
            IconProvider.icons[icon_key] = new_icon
        return new_icon


