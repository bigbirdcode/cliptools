"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Panel with a shell for more complex actions
"""

import wx

from cliptools_app import gui_show_hide_panel


class ShellPanel(gui_show_hide_panel.ShowHidePanel):

    """Shell panel"""

    def __init__(self, parent):
        super().__init__(parent, wx.HORIZONTAL, "M")

    def create_content_and_sizer(self):
        """Override: Add a shell
        panels are given, only sizer is needed"""
        shell_sizer = wx.BoxSizer(wx.VERTICAL)
        self.selected_text = wx.TextCtrl(self.show_hide_panel, -1, "Selected text",
                                         size=(500, 500), style=wx.TE_MULTILINE)
        shell_sizer.Add(self.selected_text, 1, wx.EXPAND)
        return shell_sizer

    def set_editor(self):
        """Override: set the selected text as the editor"""
        return self.selected_text
