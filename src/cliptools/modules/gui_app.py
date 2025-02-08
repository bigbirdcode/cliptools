"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

GUI App as a wx.App
"""

import wx

from cliptools.modules import gui_frame
from cliptools.modules.config import Config
from cliptools.modules.data_struct import DataCollections


class GuiLinesApp(wx.App):
    """Main GUI App"""

    def __init__(self, config: Config, data: DataCollections) -> None:
        self.config = config
        self.data = data
        super().__init__()

    def OnInit(self):
        """The wxPython calls OnInit to create widgets"""
        self.frame = gui_frame.GuiLinesFrame(
            parent=None, title="Clip Tools", config=self.config, data=self.data
        )
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        return True

    def minimize(self):
        """Minimize window"""
        self.frame.Iconize(True)

    def bring_to_front(self):
        """
        When needed window should pop up to front
        Note: popping windows are annoying, but here user pressed a hotkey to trigger it
        """
        self.frame.Show()
        self.frame.Raise()
        self.frame.Iconize(False)

    def show_hide_details_panel(self):
        """Show / hide details panel"""
        self.frame.details_panel.show_hide()

    def focus_details_panel(self):
        """Focus the editor field of details panel, show it if needed"""
        self.frame.details_panel.show()
        self.frame.details_panel.focus_editor()

    def show_hide_shell_panel(self):
        """Show / hide shell panel"""
        self.frame.shell_panel.show_hide()

    def focus_shell_panel(self):
        """Focus the shell, show it if needed"""
        self.frame.shell_panel.show()
        self.frame.shell_panel.focus_editor()
