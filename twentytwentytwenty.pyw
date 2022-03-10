# TwentyTwentyTwenty
# The 20/20/20 rule helps reduce eye strain.
# This app will remind you every 20 minutes to look at something 20 feet away for 20 seconds.

# Config
interval = 20 * 60                                      # The interval between reminders.
distance = "20 feet"                                    # The distance to look away.
duration = 20                                           # The time to look away for.
message = "Look at something {} away for {} seconds."   # The message to display.
title = "TwentyTwentyTwenty"                            # The window title.
window_size = "400x100"                                 # The window size.
message_font = "Segoe UI"                               # The font of the message.
message_font_size = 12                                  # The font size of the message.
show_start_message = True                               # Whether or not to show the start message.

import tkinter
from tkinter import messagebox
import time
import threading
import os
if os.name == "nt":
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID()

root = tkinter.Tk()

timer = None
label = None
start_time = None

def done():
    timer.cancel()

def updateLabel(start_time):
    label['text'] = message.format(distance, start_time + duration - int(time.time()))

def remind():
    start_time = int(time.time())
    updateLabel(start_time)

    # Show the window
    root.deiconify()

    # Start the timer
    global timer
    timer = threading.Timer(duration, done)
    timer.start()

    # Show the window on top
    root.attributes('-topmost', True)
    root.update()
    root.attributes('-topmost', False)

    # Main loop
    while timer.is_alive():
        updateLabel(start_time)
        root.update_idletasks()
        root.update()

    # Hide the window
    root.withdraw()

def main():
    # Hide the window
    root.withdraw()

    root.title(title)

    root.geometry(window_size)
    root.resizable(False, False)

    root.iconbitmap("icon.ico" if os.name == "nt" else "icon.png")

    # Cancel the timer if the window is closed
    root.protocol("WM_DELETE_WINDOW", done)

    # Add the message
    global label
    label = tkinter.Label(root, text=message.format(distance, duration), font=(message_font, message_font_size))
    label.place(relx = 0.5, rely = 0.5, anchor = "center")

    if show_start_message:
        with open("lang/en/start_message.txt") as start_message:
            messagebox.showinfo(title, start_message.read())

    while True:
        time.sleep(interval)
        remind()

if __name__ == "__main__":
    main()