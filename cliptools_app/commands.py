"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Key or command line commands

Commands that can be used (these are the important ones, full list is below)
    number: select line, proceed with the selection, copy as the last action
    0: minimize
    B: back
    C: copy selected text immediately
    F: bring forward, use it in base keyboard shortcut for bringing up the app
    U: page up
    D: page down
Strings are executed as Key sequence, example: 'F1C'

Key description is modifiers (if any) and basic keydown name
Examples: '1', 'Ctrl-1', 'Ctrl-Shift-Alt-1'
"""

import wx


SPECIAL_KEYS = {
    wx.WXK_BACK: 'Back',
    wx.WXK_ESCAPE: 'Esc',
    wx.WXK_PAGEUP : "Pageup",
    wx.WXK_PAGEDOWN : "Pagedown",
}

# Note: if you change NUMBER_OF_ROWS value change commands accordingly

NUM_KEYS = "123456789"

BUTTON_CODES = str.maketrans("▲▼←^", "UDBV")

KEY_COMMANDS = {
    "1": "1",  # select line, proceed with the selection, copy as the last action
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "0": "0",  # minimize
    "A": "A",  # show the about box (also the title click)
    "B": "B",  # back
    "C": "C",  # copy selected text immediately
    "D": "D",  # page down
    "F": "F",  # bring forward, use it in base keyboard shortcut for bringing up the app
    "U": "U",  # page up
    "V": "V",  # show/hide the details panel
    "Back": "B",
    "Esc": "0",
    "Pageup": "U",
    "Pagedown": "D",
    "Ctrl-1": "1C",  # select + copy the line
    "Ctrl-2": "2C",
    "Ctrl-3": "3C",
    "Ctrl-4": "4C",
    "Ctrl-5": "5C",
    "Ctrl-6": "6C",
    "Ctrl-7": "7C",
    "Ctrl-8": "8C",
    "Ctrl-9": "9C",
}
