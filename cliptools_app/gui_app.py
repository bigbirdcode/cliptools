"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Module contain the GUI codes and clipboard polling function
as part of the wx mainloop
"""

import wx
import wx.adv

from cliptools_app import gui_frame


class GuiLinesApp(wx.App):

    """Main GUI App"""

    def OnInit(self):
        """wxPython calls OnInit to create widgets"""
        self.frame = gui_frame.GuiLinesFrame(None, "Clip Tools")
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        return True

    def register_callbacks(self, handle_keyboard_events, handle_focus_event, handle_update_request):
        """Callbacks coming from controller to handle communication"""
        self.frame.handle_keyboard_events = handle_keyboard_events
        self.frame.handle_focus_event = handle_focus_event
        self.frame.handle_update_request = handle_update_request

    def minimize(self):
        """Minimize window"""
        self.frame.Iconize(True)

    def bring_to_front(self):
        """When needed window should pop up to front
        Note: popping windows are annoying, but here user pressed a hotkey to trigger it"""
        self.frame.Show()
        self.frame.Raise()
        self.frame.Iconize(False)

    def show_hide_details_panel(self):
        """Show / hide_details page"""
        self.frame.details_panel.show_hide()
