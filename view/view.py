import os
import sys
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox

from common import deputils
from common.events.events import SetPathEvent
from common.exceptions.exceptions import MvcError
from common.observer import Observer
from controller.controller import Controller
from controller.testcontroller import MockController
from view.dialogs import LayoutDialog
from view.icons import IconProvider
from view.widgets.tooltip import Tooltip


PLEASE_INSTALL_MODULES = "Please install dependency modules by doing this(use pip or pip3):\n"
dependency = 'tkfilebrowser'


deputils.check_import(dependency)

try:
    tkfilebrowser = deputils.do_import(dependency)
except ModuleNotFoundError as e:
    if e.name == 'win32com':
        error_msg = PLEASE_INSTALL_MODULES
        error_msg += f"\nC:\> pip install pywin32"
        error_msg += f"\n$ pip install pywin32"
        messagebox.showerror('Missing dependency', error_msg)
        sys.exit(0)


class GuiView(ttk.Frame, Observer):
    ROW_MINSIZE = 5
    COL_MINSIZE = 35
    PADDING = 5
    ICON_PLACE = 'right'

    def __init__(self, controller: Controller, *args, **kwargs):
        self.root = tk.Tk()
        super().__init__(master=self.root, *args, **kwargs)
        self.controller = controller
        self.selected_profile = tk.StringVar()
        self.destiny_path = tk.StringVar()
        self.destiny_path.set(f'{Path.home()}')

        # Dynamic resizing
        """
                Col0    Col1    Col2    Col3    Col4
        Row 0   ----------- Create -----------
        Row 1   Profile Cmb     Entry   SaveTo
        Row 2   --- Add ----    --------------  Yscr
        Row 3   --- Rmv ----    ---- List ----  Yscr
        Row 4   -- Clear ---    --------------  Yscr
        Row 5                   ---- Xscr ----
        Row 6   ---------- Collect -----------
        Row 7   ----------- Text -------------  Yscr
        Row 8   ----------- Xscr -------------  Yscr
        """

        rows = (0, 0, 0,
                0, 0, 0,
                0, 1, 0)
        columns = (0, 0, 1, 0, 0)
        for numrow, weight in enumerate(rows):
            self.rowconfigure(numrow, weight=weight, minsize=GuiView.ROW_MINSIZE)
        for numcol, weight in enumerate(columns):
            self.columnconfigure(numcol, weight=weight, minsize=GuiView.COL_MINSIZE)
        self.pack(fill=tk.BOTH, expand=tk.TRUE)

        # Widgets
        folder_img = IconProvider.get('open_folder')
        btn_dialog = ttk.Button(self, text='txt_btn_dialog',
                                image=folder_img, compound=GuiView.ICON_PLACE,
                                command=self._on_btn_dialog)
        Tooltip(btn_dialog, text='this button opens a dialog')
        btn_dialog.grid(row=0, column=0, columnspan=5,
                        sticky='ew', padx=GuiView.PADDING, pady=GuiView.PADDING)

        ops = Controller.get_combo_options()
        ttk.Label(self, text='txt_label').grid(row=1, column=0, padx=GuiView.PADDING, pady=GuiView.PADDING)
        cmb_profile = ttk.Combobox(self, values=ops, state='readonly',
                                   textvariable=self.selected_profile)
        Tooltip(cmb_profile, text='combobox for selecting values')
        cmb_profile.grid(row=1, column=1, sticky='we',
                         padx=GuiView.PADDING, pady=GuiView.PADDING)

        path_entry = ttk.Entry(self, textvariable=self.destiny_path,
                               state='readonly')
        path_entry.grid(row=1, column=2, sticky='we',
                        padx=GuiView.PADDING, pady=GuiView.PADDING)

        # We use an icon in this button
        save_disk_img = IconProvider.get('save_disk')
        btn_saveto = ttk.Button(self, image=save_disk_img,
                                text='txt_btn_save', compound=GuiView.ICON_PLACE,
                                command=self._on_open_save_dialog)
        Tooltip(btn_saveto, text='button for saving things')
        btn_saveto.grid(row=1, column=3, columnspan=2, sticky='we',
                        padx=GuiView.PADDING, pady=GuiView.PADDING)

        btn_add_values = ttk.Button(self, image=folder_img,
                                      compound=GuiView.ICON_PLACE,
                                      text='txt_btn_add_value',
                                      command=self._on_open_collectd_dialog)
        Tooltip(btn_add_values, text='button for add values')
        btn_add_values.grid(row=2, column=0, columnspan=2,sticky='nswe',
                              padx=GuiView.PADDING, pady=GuiView.PADDING)

        garbage_bin_img = IconProvider.get('garbage_bin')
        btn_remove_metric_paths = ttk.Button(self, image=garbage_bin_img, compound=GuiView.ICON_PLACE,
                                             text='txt_btn_remove_value',
                                             command=self._on_remove_collectd_selection)
        Tooltip(btn_remove_metric_paths, text='this button removes values')
        btn_remove_metric_paths.grid(row=3, column=0, columnspan=2,
                                     sticky='nswe', padx=GuiView.PADDING, pady=GuiView.PADDING)

        btn_clear_metric_paths = ttk.Button(self, image=garbage_bin_img, compound=GuiView.ICON_PLACE,
                                            text=f'txt_btn_clear',
                                            command=self._on_clear_collectd_selection)
        Tooltip(btn_clear_metric_paths, text='this button clears all')
        btn_clear_metric_paths.grid(row=4, column=0, columnspan=2,
                                    sticky='nswe', padx=GuiView.PADDING, pady=GuiView.PADDING)

        # Listbox with dynamic vertical scroll
        xscr = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        xscr.grid(row=5, column=2, rowspan=1, columnspan=2, sticky='WE')
        yscr = ttk.Scrollbar(self, orient=tk.VERTICAL)
        yscr.grid(row=2, rowspan=3, column=4, sticky='NS')
        self.lst_path = tk.Listbox(self, height=5,
                                   xscrollcommand=xscr.set, yscrollcommand=yscr.set)
        self.lst_path.grid(row=2, column=2, rowspan=3, columnspan=2,
                           sticky='nswe', padx=GuiView.PADDING, pady=GuiView.PADDING)
        xscr['command'] = self.lst_path.xview
        yscr['command'] = self.lst_path.yview

        metrics_img = IconProvider.get('metrics')
        btn_collect = ttk.Button(self, text='txt_btn_dothings',
                                 image=metrics_img, compound=GuiView.ICON_PLACE,
                                 command=self._on_collect_metrics)
        Tooltip(btn_collect, text='this button gets the stuff done')
        btn_collect.grid(row=6, column=0, columnspan=5,
                         sticky='we', padx=GuiView.PADDING, pady=GuiView.PADDING)

        # Text widget with dynamic scroll
        xscr = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        xscr.grid(row=8, column=0, columnspan=4, sticky='WE')
        yscr = ttk.Scrollbar(self, orient=tk.VERTICAL)
        yscr.grid(row=7, column=4, sticky='NS')
        self.output = tk.Text(self, height=8,
                              yscrollcommand=yscr.set,
                              xscrollcommand=xscr.set)
        self.output.configure(state=tk.DISABLED)
        self.output.grid(row=7, column=0, columnspan=4,
                         sticky='nswe', padx=GuiView.PADDING, pady=GuiView.PADDING)
        yscr['command'] = self.output.yview
        xscr['command'] = self.output.xview

    def init_ui(self):
        self.root.title('MyProject')
        self.root.withdraw()
        self.root.iconify()
        self.root.update()
        self.root.deiconify()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        self.root.mainloop()

    def start(self):
        self.init_ui()

    def update(self, value):
        msg = '\n'
        if isinstance(value, str):
            msg += value
        elif isinstance(value, MvcError):
            msg += value.messages[0]
            messagebox.showerror('Error', msg)
        elif isinstance(value, SetPathEvent):
            self.destiny_path.set(value.info)

        if msg.strip():
            self.output.config(state=tk.NORMAL)
            self.output.insert(tk.END, msg)
            self.output.config(state=tk.DISABLED)

    def _on_collect_metrics(self):
        """
        Handles event when the collect metrics button is pressed
        :param __: the event
        """
        self.controller.collect_metrics(self.destiny_path.get(),
                                        self.lst_path.get(0, tk.END),
                                        self.selected_profile.get())

    def _on_open_save_dialog(self, __=None):
        """
        Handles event when the save button is pressed
        :param __: the event
        """
        self.destiny_path.set(
            tkfilebrowser.askopendirname(initialdir=self.destiny_path.get(),
                                         title='txt_enter_path')
        )

    def _on_open_collectd_dialog(self, __=None):
        """
        Handles event when the add metrics button is pressed
        :param __: the event
        """
        initial_dir = ''
        dest_path = self.destiny_path.get()
        if dest_path and dest_path.strip():
            initial_dir = os.path.dirname(dest_path)

        upper_selected_profile = self.selected_profile.get().upper()
        top_title_msg = 'txt_title_{}'.format(upper_selected_profile)
        collectd_paths = tkfilebrowser.askopendirnames(initialdir=initial_dir,
                                                       title=top_title_msg)
        for p in collectd_paths:
            self.lst_path.insert(tk.END, p)

    def _on_remove_collectd_selection(self, __=None):
        """
        Handles event when the remove metrics path button is pressed
        :param __: the event
        """
        for idx in self.lst_path.curselection():
            self.lst_path.delete(idx)

    def _on_clear_collectd_selection(self, __=None):
        """
        Handles event when the clear button is pressed
        :param __: the event
        """
        self.lst_path.delete(0, tk.END)

    def _on_btn_dialog(self, __=None):
        """
        Handles event when the clear button is pressed
        :param __: the event
        """
        try:
            d = LayoutDialog(self)
        except MvcError as ge:
            self.update(ge)


if __name__ == '__main__':
    v = GuiView(MockController())
    v.init_ui()

