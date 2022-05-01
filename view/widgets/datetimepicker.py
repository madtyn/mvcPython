"""
Widget for managing the input for both date and time
"""

import datetime as dt

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from .timepicker import Timepicker



class DatetimePicker(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        """
        Initializes this datetime component

        :param parent: the parent
        :param args: the arguments
        :param kwargs: the kwargs
        """
        super().__init__(parent)
        self.parent = parent

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)

        self.dateformat = 'dd/mm/y'
        if 'dateformat' in kwargs:
            self.dateformat = kwargs.get('dateformat')

        self.date = DateEntry(self, date_pattern=self.dateformat, *args, **kwargs)
        self.time = Timepicker(self, *args, **kwargs)
        self.date.grid(row=0, column=0, sticky='we', padx=2)
        self.time.grid(row=0, column=1, padx=2)

    def get_date(self):
        """
        Gets only the date from this widget, omitting the time

        :return: the date
        """
        return self.date._date

    def get_time(self):
        """
        Gets only the time from this widget, omitting the date

        :return: the time
        """
        return self.time.get_time()

    def get_datetime(self, as_string=False):
        """
        Gets the whole datetime contained in this widget

        :param as_string: True for returning a string, datetime by default
        :return: the datetime
        """
        result = dt.datetime.combine(self.get_date(), self.get_time())
        if as_string:
            result = result.strftime('%Y-%m-%d %H:%M')
        return result

    def validate(self):
        """
        Validates the whole datetime contained in this widget

        :return: True if correct, False otherwise
        """
        if self.get_date() is None:
            return False

        return self.time.validate_time()


if __name__ == '__main__':
    root = tk.Tk()
    DatetimePicker(root).pack()
    root.mainloop()
