"""
Module for dialogs
"""

import datetime as dt
import sys

import tkinter as tk
from pathlib import Path
from tkinter import ttk
from tkinter.simpledialog import Dialog
from tkinter.ttk import Label, Entry


from common import deputils
from common.constants import MISSING_DEPENDENCIES_ERROR_CODE
from common.exceptions.exceptions import MvcError
from common.utils import ROOT_PATH
from view.widgets.tooltip import Tooltip
from .icons import IconProvider
from .widgets.datetimepicker import DatetimePicker

PLEASE_INSTALL_MODULES = "Please install dependency modules by doing this(use pip or pip3):\n"


dependency = 'tkfilebrowser'

try:
    tkfilebrowser = deputils.do_import(dependency)
except ModuleNotFoundError as e:
    if e.name == 'win32com':
        print(PLEASE_INSTALL_MODULES)
        print("C:\\> pip install pywin32")
        print("$ pip install pywin32")
        sys.exit(MISSING_DEPENDENCIES_ERROR_CODE)


class LayoutDialog(Dialog):
    """
    Class for the dialog in which we ask for data so that
    we can create the folder layout
    """
    CAPTION_ICON_POS = 'left'
    DEFAULT_PADDING = 5
    SELECT_PATH_ROW = 0
    ENTRY_LAYOUT_PATH_ROW = 1
    PROJECT_DESC_ROW = 2
    DATETIME_ROW = 3
    SELECT_TEMPLATE_FILE_ROW = 4
    ENTRY_TEMPLATE_PATH_ROW = 5

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        """
        Because parent class does body before this __init__
        some ugly hacks are needed here so that PyCharm doesn't complain
        about fields not being set in __init__
        """
        if not hasattr(self, 'field1'):
            self.field1 = tk.StringVar()
        if not hasattr(self, 'field2'):
            self.field2 = tk.StringVar()
        if not hasattr(self, 'path1'):
            self.path1 = tk.StringVar()
        if not hasattr(self, 'path2'):
            self.path2 = tk.StringVar()
        if not hasattr(self, 'field3'):
            self.field3 = tk.StringVar()
        if not hasattr(self, 'datetime'):
            self.datetime = None
            raise MvcError(['Datetime picker error'])

    def body(self, master):
        super().body(master)
        self.title('txt_btn_create_layout')

        master.rowconfigure(LayoutDialog.SELECT_PATH_ROW, weight=0)
        master.rowconfigure(LayoutDialog.SELECT_TEMPLATE_FILE_ROW, weight=0)
        master.rowconfigure(LayoutDialog.ENTRY_LAYOUT_PATH_ROW, weight=0)
        master.rowconfigure(LayoutDialog.PROJECT_DESC_ROW, weight=0)
        master.rowconfigure(LayoutDialog.DATETIME_ROW, weight=0)
        master.columnconfigure(0, weight=0)
        master.columnconfigure(1, weight=0)
        master.columnconfigure(2, weight=1)
        master.columnconfigure(3, weight=0)

        self.field1 = tk.StringVar()
        self.field2 = tk.StringVar()
        self.field3 = tk.StringVar()
        self.path1 = tk.StringVar()
        self.path1.set(f'{Path.home()}')
        self.path2 = tk.StringVar()
        self.path2.set(f'{Path.home()}')

        # Row
        btn_projects_dir = ttk.Button(master, text='txt_btn_projects_path',
                                      image=IconProvider.get('open_folder'),
                                      compound=LayoutDialog.CAPTION_ICON_POS,
                                      command=self._on_open_save_dialog)
        Tooltip(btn_projects_dir, text='txt_ttip_projects_path')
        btn_projects_dir.grid(row=LayoutDialog.SELECT_PATH_ROW,
                              column=0, columnspan=4, sticky='we',
                              padx=LayoutDialog.DEFAULT_PADDING,
                              pady=LayoutDialog.DEFAULT_PADDING)

        # Row
        ttk.Entry(master, textvariable=self.path1, state='readonly').grid(row=LayoutDialog.ENTRY_LAYOUT_PATH_ROW, sticky='we', column=0, columnspan=4, padx=LayoutDialog.DEFAULT_PADDING, pady=LayoutDialog.DEFAULT_PADDING)

        # Row
        btn_template_file = ttk.Button(master, text='txt_btn_select_template_path',
                                       image=IconProvider.get('open_folder'),
                                       compound=LayoutDialog.CAPTION_ICON_POS,
                                       command=self._on_open_select_template)
        Tooltip(btn_template_file, text='txt_ttip_select_template_path')
        btn_template_file.grid(row=LayoutDialog.SELECT_TEMPLATE_FILE_ROW,
                               column=0, columnspan=4, sticky='we',
                               padx=LayoutDialog.DEFAULT_PADDING,
                               pady=LayoutDialog.DEFAULT_PADDING)

        # Row
        ttk.Entry(master, textvariable=self.path2, state='readonly').grid(row=LayoutDialog.ENTRY_TEMPLATE_PATH_ROW,
                                                                          sticky='we', column=0, columnspan=4,
                                                                          padx=LayoutDialog.DEFAULT_PADDING,
                                                                          pady=LayoutDialog.DEFAULT_PADDING)

        # Row
        Label(master, text="JIRA Code").grid(row=LayoutDialog.PROJECT_DESC_ROW, column=0, padx=LayoutDialog.DEFAULT_PADDING, pady=LayoutDialog.DEFAULT_PADDING)
        ent_prefix = Entry(master, width=6, textvariable=self.field1)
        Tooltip(ent_prefix, text='txt_ttip_prefix')
        ent_prefix.grid(row=LayoutDialog.PROJECT_DESC_ROW, column=1, padx=LayoutDialog.DEFAULT_PADDING, pady=LayoutDialog.DEFAULT_PADDING)

        ent_project = Entry(master, width=16, textvariable=self.field2)
        Tooltip(ent_project, text='txt_ttip_project')
        ent_project.grid(row=LayoutDialog.PROJECT_DESC_ROW, column=2, padx=LayoutDialog.DEFAULT_PADDING, pady=LayoutDialog.DEFAULT_PADDING)

        ent_suffix = Entry(master, width=6, textvariable=self.field3)
        Tooltip(ent_suffix, text='txt_ttip_suffix')
        ent_suffix.grid(row=LayoutDialog.PROJECT_DESC_ROW, column=3, padx=LayoutDialog.DEFAULT_PADDING, pady=LayoutDialog.DEFAULT_PADDING)
        # Row
        Label(master, text='txt_lbl_datetime').grid(row=LayoutDialog.DATETIME_ROW, column=0, padx=LayoutDialog.DEFAULT_PADDING, pady=LayoutDialog.DEFAULT_PADDING)
        today = dt.datetime.today()
        self.datetime = DatetimePicker(master,
                                       day=today.day, month=today.month,
                                       year=today.year, hour=today.hour,
                                       minute=today.minute,
                                       dateformat='dd/mm/y')

        self.datetime.grid(row=LayoutDialog.DATETIME_ROW, column=1, sticky='we', columnspan=3, padx=LayoutDialog.DEFAULT_PADDING, pady=LayoutDialog.DEFAULT_PADDING)
        self.resizable(False, False)
        return ent_prefix

    def validate(self):
        project_path = Path(self.path1.get())
        if not project_path.exists() or not project_path.is_dir():
            return False

        if any(x.get().strip() == '' for x in (self.field1, self.field2, self.field3)):
            return False

        return self.datetime.validate()

    def _on_open_save_dialog(self, __=None):
        """
        Handles event when the save button is pressed
        :param __: the event
        """
        self.path1.set(
            tkfilebrowser.askopendirname(initialdir=self.path1.get(),
                                         title='txt_title_select_layout_path')
        )

    def _on_open_select_template(self, __=None):
        """
        Handles event when the select template button is pressed
        :param __: the event
        """
        input_filetypes = (("My kind of file", "*.kind|*.file"),)

        self.path2.set(
            tkfilebrowser.askopenfilename(initialdir=ROOT_PATH,
                                          title='txt_title_select_report_path',
                                          filetypes=input_filetypes)
        )


if __name__ == '__main__':
    root = tk.Tk()
    d = LayoutDialog(root)
    print(d.datetime.get_date())
