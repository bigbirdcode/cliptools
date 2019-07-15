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
    wx.WXK_PAGEUP: "Pageup",
    wx.WXK_PAGEDOWN: "Pagedown",
    wx.WXK_UP: "Up",
    wx.WXK_DOWN: "Down",
    wx.WXK_LEFT: "Left",
    wx.WXK_RIGHT: "Right",
}

# Note: if you change NUMBER_OF_ROWS value change commands accordingly

NUM_KEYS = "123456789"

BUTTON_CODES = str.maketrans("▲▼←^", "UDBV")

KEY_COMMANDS = {
    # select line, proceed with the selection, copy as the last action
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    # Minimize
    "0": "0",
    # WASD controls, plus QE for pages
    "A": "A",  # back
    "D": "D",  # forward
    "W": "W",  # step up
    "S": "S",  # step down
    "E": "E",  # page down (forward in the list)
    "Q": "Q",  # page up (back in the list)
    # Other actions
    "F": "F",  # bring forward, use it in base keyboard shortcut for bringing up the app
    "C": "C",  # copy selected text immediately
    "V": "V",  # copy processed text immediately
    "I": "I",  # show the info dialog (also the title click)
    "Z": "Z",  # show/hide the details panel
    # Aliases
    "Back": "A",
    "B": "A",
    "Esc": "0",
    "Up": "W",
    "Down": "S",
    "Left": "A",
    "Right": "D",
    "Pageup": "Q",
    "Pagedown": "E",
    # Scripts
    "Ctrl-1": "1C",  # select + copy the line
    "Ctrl-2": "2C",
    "Ctrl-3": "3C",
    "Ctrl-4": "4C",
    "Ctrl-5": "5C",
    "Ctrl-6": "6C",
    "Ctrl-7": "7C",
    "Ctrl-8": "8C",
    "Ctrl-9": "9C",
    "Shift-1": "1V",  # select the line + copy the processed line
    "Shift-2": "2V",
    "Shift-3": "3V",
    "Shift-4": "4V",
    "Shift-5": "5V",
    "Shift-6": "6V",
    "Shift-7": "7V",
    "Shift-8": "8V",
    "Shift-9": "9V",
}
