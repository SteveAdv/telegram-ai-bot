import tkinter as tk
from datetime import datetime
import pytz

class DigitalClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Clock")

        self.timezones = ['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo']
        self.label = tk.Label(root, font=("Helvetica", 48), bg="black", fg="white")
        self.label.pack(anchor='center')

        self.dropdown = tk.StringVar()
        self.dropdown.set(self.timezones[0])
        self.option_menu = tk.OptionMenu(root, self.dropdown, *self.timezones, command=self.update_clock)
        self.option_menu.pack(anchor='s')

        self.update_clock(self.timezones[0])

    def update_clock(self, timezone):
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        self.label.config(text=current_time)
        self.root.after(1000, self.update_clock, timezone)

if __name__ == '__main__':
    root = tk.Tk()
    clock = DigitalClock(root)
    root.mainloop()