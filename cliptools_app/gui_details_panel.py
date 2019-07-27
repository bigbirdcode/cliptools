"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Details panel are an addition, it will show the selected text, function help and processed text
"""

import wx

from cliptools_app import gui_show_hide_panel

class DetailsPanel(gui_show_hide_panel.ShowHidePanel):

    """Details panel with 3 multi line text to show
    the selected text, function help and processed text"""

    def __init__(self, parent):
        super().__init__(parent, wx.VERTICAL, "Z")

        # Add 3 multi-line text for the details
        # panels are given, only sizer is needed
        details_sizer = wx.BoxSizer(wx.VERTICAL)
        self.selected_text = wx.TextCtrl(self.show_hide_panel, -1, "Selected text",
                                         size=(200, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.action_doc = wx.TextCtrl(self.show_hide_panel, -1, "Help for the action",
                                      size=(200, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.processed_text = wx.TextCtrl(self.show_hide_panel, -1, "Processed text",
                                          size=(200, 100), style=wx.TE_MULTILINE|wx.TE_READONLY)
        details_sizer.Add(self.selected_text, 1, wx.EXPAND)
        details_sizer.Add(self.action_doc, 1, wx.EXPAND)
        details_sizer.Add(self.processed_text, 1, wx.EXPAND)
        self.show_hide_panel.SetSizer(details_sizer)

        # Set the layout in the panel
        self.Fit()

    def update_data(self, selected_text, action_doc, processed_text):
        """Update the details texts"""
        self.selected_text.Clear()
        self.selected_text.AppendText(selected_text)
        self.selected_text.SetInsertionPoint(0)
        self.action_doc.Clear()
        self.action_doc.AppendText(action_doc)
        self.action_doc.SetInsertionPoint(0)
        self.processed_text.Clear()
        self.processed_text.AppendText(processed_text)
        self.processed_text.SetInsertionPoint(0)
