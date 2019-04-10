"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Key or command line commands

Commands that can be used
    number: select line
    0: minimize
    b: back
    c: copy immediately
    f: bring forward, use it in base keyboard shortcut for bringing up the app
Strings are executed as Key sequence, example: 'f1c'

Key description is modifiers (if any) and basic keydown name
Examples: '1', 'Shift-1', 'Shift-Ctrl-Alt-1'
"""

import wx


SPECIAL_KEYS = {
    wx.WXK_BACK: 'Back',
    wx.WXK_ESCAPE: 'Esc',
}

# Note: if you change NUMBER_OF_ROWS value change commands accordingly

NUM_KEYS = "123456789"

KEY_COMMANDS = {
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "0": "0",
    "b": "b",
    "c": "c",
    "f": "f",
    "Back": "b",
    "Esc": "0",
    "Shift-1": "1c",
    "Shift-2": "2c",
    "Shift-3": "3c",
    "Shift-4": "4c",
    "Shift-5": "5c",
    "Shift-6": "6c",
    "Shift-7": "7c",
    "Shift-8": "8c",
    "Shift-9": "9c",
}
