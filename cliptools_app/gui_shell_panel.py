"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Module contain the GUI codes and clipboard polling function
as part of the wx mainloop
"""

import wx
import wx.adv

from cliptools_app import gui_show_hide_panel


class ShellPanel(gui_show_hide_panel.ShowHidePanel):

    """Create the main panel with the lines and the details sub-panel"""

    def __init__(self, parent):
        super().__init__(parent, wx.HORIZONTAL, "M")

        self.parent = parent

        # panel for the additional shell
        shell_sizer = wx.BoxSizer(wx.VERTICAL)
        tmp_btn = wx.Button(self.show_hide_panel, -1, "Shell", size=(30, 30), name="T")
        shell_sizer.Add(tmp_btn, 1, wx.EXPAND)
        self.show_hide_panel.SetSizer(shell_sizer)

        self.Fit()
