"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Module contain the GUI codes and clipboard polling function
as part of the wx mainloop
"""

from itertools import chain, repeat

import wx
import wx.adv

from config import NUMBER_OF_ROWS


class LinesPanel(wx.Panel):

    """Create the main panel with the lines and the details sub-panel"""

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.parent = parent

        # List of textboxes for easier reference
        self.texts = list()

        # Colors to use for the lines
        self.active_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        self.normal_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)

        # Use a sizer to layout the controls, stacked vertically
        # lines and the details panel are the main parts of it
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Buttons in the top row, back, page, instructions
        subsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, -1, "←", size=(25, 25), name="A")
        subsizer.Add(btn, 0, wx.CENTER)
        self.title_btn = wx.Button(self, -1, "Title", size=(25, 25), name="I")
        subsizer.Add(self.title_btn, 1, wx.CENTER)
        btn = wx.Button(self, -1, "▲", size=(25, 25), name="Q")
        subsizer.Add(btn, 0, wx.CENTER)
        btn = wx.Button(self, -1, "▼", size=(25, 25), name="E")
        subsizer.Add(btn, 0, wx.CENTER)
        sizer.Add(subsizer, 0, wx.EXPAND)

        # Add the lines: 1 button 1 text
        # Use a sizer to layout the controls,
        # Name numbering starts from 1 to match key presses
        for i in range(NUMBER_OF_ROWS):
            num_name = str(i+1)
            subsizer = wx.BoxSizer(wx.HORIZONTAL)
            btn = wx.Button(self, -1, num_name, size=(25, 25), name=num_name)
            subsizer.Add(btn, 0, wx.CENTER)
            text = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY, size=(200, -1), name=num_name)
            subsizer.Add(text, 1, wx.EXPAND)
            sizer.Add(subsizer, 0, wx.EXPAND)
            self.texts.append(text)
            text.Bind(wx.EVT_LEFT_UP, self.on_mouse_click)
            btn.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)
            text.Bind(wx.EVT_ENTER_WINDOW, self.on_enter)

        self.SetSizer(sizer)
        self.Fit()

    def update_data(self, title, data_iter, focus_number):
        """Update the line data from the provided generator/iterator
        Beside also update details texts and line focus"""
        # Title shows where are we now
        self.title_btn.SetLabel(title)
        # Lines show the actual texts
        for i, text in enumerate(chain(data_iter, repeat(""))):
            if i >= NUMBER_OF_ROWS:
                break
            entry = self.texts[i]
            entry.Clear()
            entry.AppendText(text)
            entry.SetInsertionPoint(0)
            if i == focus_number:
                entry.SetBackgroundColour(self.active_color)
                entry.SetFocus()
            else:
                entry.SetBackgroundColour(self.normal_color)

    def on_mouse_click(self, event):
        """Mouse clicks on the text lines.
        Task delegated to controller based on name"""
        obj_name = event.GetEventObject().GetName()
        try:
            if int(obj_name) > 0:
                self.parent.handle_keyboard_events(obj_name)
        except ValueError:
            pass  # it was not a line, but something else
        event.Skip()

    def on_enter(self, event):
        """Mouse-over handler, delegating tasks to focus handler"""
        obj_name = event.GetEventObject().GetName()
        try:
            if int(obj_name) > 0:
                self.parent.handle_focus_event(obj_name)
        except ValueError:
            pass  # it was not a line, but something else
        event.Skip()
