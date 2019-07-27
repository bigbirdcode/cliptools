"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Abstract panel with a button and a sub-panel that can be shown or hidden
can be vertical or horizontal, need a sizer and to fit in children
"""

import wx

from cliptools_app import gui_tools


class ShowHidePanel(wx.Panel):

    """An abstract panel that can show the content or hide with a button.

    Children should define the contents in a sizer and
    define the editor if there is one.
    """

    def __init__(self, parent, layout, key_code):
        """ A panel that can show the content or hide with a button.

        layout is either wx.VERTICAL or wx.HORIZONTAL
        key_code is the code name for the main button
        """
        wx.Panel.__init__(self, parent, -1)

        self.open_title = "^" if layout == wx.VERTICAL else "<"
        self.closed_title = "v" if layout == wx.VERTICAL else ">"

        # Use a sizer to layout the controls
        sizer = wx.BoxSizer(layout)

        # button to open the content
        self.show_hide_btn = wx.Button(self, -1, self.closed_title, size=(15, 15), name=key_code)
        sizer.Add(self.show_hide_btn, 0, wx.EXPAND)

        # Add panel for the content
        self.show_hide_panel = wx.Panel(self)

        sub_sizer = self.create_content_and_sizer()
        self.show_hide_panel.SetSizer(sub_sizer)

        sizer.Add(self.show_hide_panel, 1, wx.EXPAND)
        self.show_hide_panel.Hide()

        # Define editor in the children to enable focus and keyboard input for them
        self.editor = self.set_editor()
        if self.editor:
            self.editor.Bind(wx.EVT_SET_FOCUS, self.on_editor_set_focus)
            self.editor.Bind(wx.EVT_KILL_FOCUS, self.on_editor_kill_focus)
            self.editor.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

        # Set the sizer, child objects should call fit
        self.SetSizer(sizer)

    def create_content_and_sizer(self):
        """Abstract function, children should overwrite
        Below is an example how it should look
        widgets should have self.show_hide_panel as the parent"""
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.my_text = wx.TextCtrl(self.show_hide_panel, -1, "My text",
                                   size=(100, 100), style=wx.TE_MULTILINE)
        sizer.Add(self.my_text, 1, wx.EXPAND)
        return sizer

    def set_editor(self):
        """Abstract function that should return the editor widget"""
        # Example:
        # return self.my_text
        return None

    def show_hide(self):
        """Show or hide the content panel"""
        visible = not self.show_hide_panel.IsShown()
        self.show_hide_btn.SetLabel(self.open_title if visible else self.closed_title)
        self.show_hide_panel.Show(visible)
        self.GetParent().Fit()

    def show(self):
        """Show the content panel"""
        if not self.show_hide_panel.IsShown():
            self.show_hide()

    def focus_editor(self):
        """Set the focus on the editor"""
        if self.editor:
            self.editor.SetFocus()

    def on_editor_set_focus(self, event):
        """Called when editor gets the focus"""
        self.GetParent().edit_mode = True
        event.Skip()

    def on_editor_kill_focus(self, event):
        """Called when editor lost the focus
        Default focus lost is done editing. You can override."""
        self.on_editor_done(event)
        event.Skip()

    def on_key_press(self, event):
        """Keyboard event handler to check for Esc press, to exit from edit mode"""
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            # do not propagate the esc key press
            self.on_editor_done(event)
        else:
            event.Skip()

    def on_editor_done(self, event):
        """Called when user is done with the edit, i.e. pressed escape or focus lost"""
        self.GetParent().edit_mode = False
        text = self.editor.GetValue()
        self.GetParent().handle_new_text(text)
        # Safe solution, select the show-hide button
        self.show_hide_btn.SetFocus()
