"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Panel with a shell for more complex actions
"""

import wx
import wx.py.shell

from . import data_struct
from . import gui_show_hide_panel


INTRO = '''*** Cliptools Shell ***
To reach the collected clips type: "clips", example: "clips.content[0]"
To reach the entire data collection type "dc"'''

class ShellPanel(gui_show_hide_panel.ShowHidePanel):

    """Shell panel"""

    def __init__(self, parent):
        super().__init__(parent, wx.HORIZONTAL, "M")

    def create_content_and_sizer(self):
        """Override: Add a shell
        panels are given, only sizer is needed"""
        shared_locals = {
            'dc': data_struct.data_collections,
            'clips': data_struct.data_collections.clip
        }
        shell_sizer = wx.BoxSizer(wx.VERTICAL)
        self.shell = wx.py.shell.Shell(self.show_hide_panel, -1, size=(500, 500), introText=INTRO, locals=shared_locals)
        shell_sizer.Add(self.shell, 1, wx.EXPAND)
        return shell_sizer

    def set_editor(self):
        """Override: set the selected text as the editor"""
        return self.shell

    def on_editor_kill_focus(self, event):
        """Override: shell lost focus on auto complete, so need to skip this.
        THIS IS A LIMITATION!
        Called when editor gets the focus
        """
        event.Skip()

    def on_editor_done(self, event):
        """Override: copy result not possible!!!
        Use selection then Ctrl+C in the shell window.
        Cliptools will collect these texts too.
        Called when user is done with the edit, i.e. pressed escape or focus lost"""
        self.GetParent().edit_mode = False
        # Safe solution, select the show-hide button
        self.show_hide_btn.SetFocus()
