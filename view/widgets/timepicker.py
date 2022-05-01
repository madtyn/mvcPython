import time
import datetime as dt

import tkinter as tk
from tkinter import ttk


class Timepicker(ttk.Frame):
    DAY_HOURS = 24
    MAX_HOUR = 23
    MAX_MINUTES = 59

    def __init__(self, parent, hour=None, minute=None, *args, **kwargs):
        super().__init__(parent)
        if not hour:
            hour = int(time.strftime('%H'))
        self.parent = parent
        self.hourstr = tk.StringVar(self, f'{hour:02}')
        self.hour = ttk.Spinbox(self, from_=0, to=23, wrap=True, name='hourspin',
                               textvariable=self.hourstr, width=4, format='%02.0f')
        vcmd = (parent.register(self._validate_hour), '%P')
        self.hour.configure(validate='key', validatecommand=vcmd)

        if not minute:
            minute = int(time.strftime('%M'))
        self.minstr = tk.StringVar(self, f'{minute:02}')
        self.minstr.trace("w", self.trace_var)
        self.last_value = f'{self.minstr.get()}'
        self.min = ttk.Spinbox(self, from_=0, to=59,  wrap=True, name='minspin',
                              textvariable=self.minstr, width=4, format='%02.0f')
        vcmd = (parent.register(self._validate_minutes), '%P')
        self.min.configure(validate='key', validatecommand=vcmd)

        self.hour.grid(row=0, column=0)
        ttk.Label(self, text=':').grid(row=0, column=1)
        self.min.grid(row=0, column=2)

    def trace_var(self, *args):
        """
        Traces the variables so that when minutes exceed 59 we add 1 to hours
        and when minutes decrease from 0 to 59 we substract 1 from hours
        :param args: the args
        """
        if self.last_value == f"{Timepicker.MAX_MINUTES}" and self.minstr.get().strip() and int(self.minstr.get()) == 0:
            self.hourstr.set(f'{(int(self.hourstr.get()) + 1) % Timepicker.DAY_HOURS:02}')
        elif self.last_value.strip() and int(self.last_value) == 0 and self.minstr.get() == f"{Timepicker.MAX_MINUTES}":
            self.hourstr.set(f'{(int(self.hourstr.get()) - 1) % Timepicker.DAY_HOURS:02}')
        self.last_value = self.minstr.get()

    def _validate_hour(self, new_value):
        """
        Validates every key press from a blank state so that no character
        entered makes the input illegal
        :param new_value: the new_value as it would be with the new character
        :return: True if we allow the edit to happen, False to prevent it
        """
        if new_value == '':
            return True

        result = self._validate_generic(new_value, Timepicker.MAX_HOUR)
        return result

    def _validate_minutes(self, new_value):
        """
        Validates every key press from a blank state so that no character
        entered makes the input illegal
        :param new_value: the new_value as it would be with the new character
        :return: True if we allow the edit to happen, False to prevent it
        """
        if new_value == '':
            return True

        result = self._validate_generic(new_value, Timepicker.MAX_MINUTES)
        return result

    def _validate_generic(self, new_value, maxvalue):
        """
        Validates that new_value is a two-figure number
        less or equal than maxvalue
        :param new_value: the new_value
        :param maxvalue: the maxvalue we won't exceed
        :return: True if this validates, False otherwise
        """
        if not new_value.isdigit():
            return False

        return len(new_value) <= 2 \
                  and 0 <= int(new_value) <= maxvalue

    def validate_time(self):
        hour_value = self.hourstr.get().strip()
        if hour_value == '' or not self._validate_hour(hour_value):
            return False

        minute_value = self.minstr.get().strip()
        if minute_value == '' or not self._validate_minutes(minute_value):
            return False
        return True

    def get_time(self):
        return dt.time(int(self.hourstr.get()), int(self.minstr.get()), 0, 0)


if __name__ == '__main__':
    root = tk.Tk()
    Timepicker(root).pack()
    root.mainloop()
