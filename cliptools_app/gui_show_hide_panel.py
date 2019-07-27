"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Module contain the GUI codes and clipboard polling function
as part of the wx mainloop
"""

import wx
import wx.adv


class ShowHidePanel(wx.Panel):

    """ A panel that can show the content or hide with a button. """

    def __init__(self, parent, layout, key_code):
        """ A panel that can show the content or hide with a button.

        layout is either wx.VERTICAL or wx.HORIZONTAL
        key_code is the code name for the main button
        """
        wx.Panel.__init__(self, parent, -1)

        self.parent = parent
        self.open_title = "^" if layout == wx.VERTICAL else "<"
        self.closed_title = "v" if layout == wx.VERTICAL else ">"

        # Use a sizer to layout the controls, stacked vertically
        sizer = wx.BoxSizer(layout)

        # button to open the content
        self.show_hide_btn = wx.Button(self, -1, self.open_title, size=(15, 15), name=key_code)
        sizer.Add(self.show_hide_btn, 0, wx.EXPAND)

        # Add panel for the content
        self.show_hide_panel = wx.Panel(self)
        sizer.Add(self.show_hide_panel, 1, wx.EXPAND)
        self.show_hide_panel.Hide()

        # Set the sizer, child objects should call fit
        self.SetSizer(sizer)

    def show_hide(self):
        """Show or hide the details panel,
        where 3 multi-line text show the selections"""
        visible = self.show_hide_panel.IsShown()
        self.show_hide_btn.SetLabel(self.open_title if visible else self.closed_title)
        self.show_hide_panel.Show(not visible)
        self.parent.Fit()
