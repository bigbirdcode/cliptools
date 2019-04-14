"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Key or command line commands

Commands that can be used
    number: select line, proceed with the selection, copy as the last action
    0: minimize
    B: back
    C: copy selected text immediately
    F: bring forward, use it in base keyboard shortcut for bringing up the app
    U: page up
    D: page down
Strings are executed as Key sequence, example: 'F1C'

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
    "B": "B",
    "C": "C",
    "F": "F",
    "D": "D",
    "U": "U",
    "Back": "B",
    "Esc": "0",
    "Shift-1": "1C",
    "Shift-2": "2C",
    "Shift-3": "3C",
    "Shift-4": "4C",
    "Shift-5": "5C",
    "Shift-6": "6C",
    "Shift-7": "7C",
    "Shift-8": "8C",
    "Shift-9": "9C",
}
