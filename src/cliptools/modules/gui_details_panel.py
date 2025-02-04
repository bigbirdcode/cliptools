"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Details panel are an addition, it will show the selected text, function help and processed text
"""

import wx

from cliptools.modules import gui_show_hide_panel


class DetailsPanel(gui_show_hide_panel.ShowHidePanel):
    """Details panel with 3 multi line text to show
    the selected text, function help and processed text"""

    def __init__(self, parent):
        super().__init__(parent, wx.VERTICAL, "Z")

    def create_content_and_sizer(self):
        """Override: Add 3 multi-line text for the details
        panels are given, only sizer is needed"""
        details_sizer = wx.BoxSizer(wx.VERTICAL)
        self.selected_text = wx.TextCtrl(
            self.show_hide_panel, -1, "Selected text", size=(200, 100), style=wx.TE_MULTILINE
        )
        self.action_doc = wx.TextCtrl(
            self.show_hide_panel,
            -1,
            "Help for the action",
            size=(200, 100),
            style=wx.TE_MULTILINE | wx.TE_READONLY,
        )
        self.processed_text = wx.TextCtrl(
            self.show_hide_panel,
            -1,
            "Processed text",
            size=(200, 100),
            style=wx.TE_MULTILINE | wx.TE_READONLY,
        )
        details_sizer.Add(self.selected_text, 1, wx.EXPAND)
        details_sizer.Add(self.action_doc, 1, wx.EXPAND)
        details_sizer.Add(self.processed_text, 1, wx.EXPAND)
        return details_sizer

    def set_editor(self):
        """Override: set the selected text as the editor"""
        return self.selected_text

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

    def on_editor_set_focus(self, event):
        """Override: add color,
        Called when editor gets the focus"""
        self.editor.SetBackgroundColour(self.GetParent().active_color)
        super().on_editor_set_focus(event)

    def on_editor_done(self, event):
        """Override: add color,
        Called when user is done with the edit, i.e. pressed escape or focus lost"""
        self.editor.SetBackgroundColour(self.GetParent().normal_color)
        super().on_editor_done(event)
