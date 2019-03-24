"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Key or command line commands
"""

import wx

from config import NUMBER_OF_ROWS

# Character keys that can also be used as command line options

NUM_KEYS = "".join(str(i) for i in range(1, NUMBER_OF_ROWS + 1))  # numbers
CONTROL_KEYS = [
    '0', # minimize
    'b', # back
    'c', # copy immediately
    'f', # bring forward, use it in base keyboard shortcut for the app
]
ALL_KEYS = NUM_KEYS + "".join(CONTROL_KEYS)


# Special keys and their meaning, i.e. macro

SPECIAL_KEYS = {
    wx.WXK_BACK: ['b'],
    wx.WXK_ESCAPE: ['0'],
    wx.WXK_F1: ['1', 'c'],
    wx.WXK_F2: ['2', 'c'],
    wx.WXK_F3: ['3', 'c'],
    wx.WXK_F4: ['4', 'c'],
    wx.WXK_F5: ['5', 'c'],
    wx.WXK_F6: ['6', 'c'],
    wx.WXK_F7: ['7', 'c'],
    wx.WXK_F8: ['8', 'c'],
    wx.WXK_F9: ['9', 'c'],
}
