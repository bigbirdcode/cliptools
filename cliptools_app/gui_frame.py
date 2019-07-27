"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Module contain the GUI codes and clipboard polling function
as part of the wx mainloop
"""

import wx
import wx.adv

from cliptools_app import commands
from cliptools_app import gui_tools
from cliptools_app import gui_lines_panel
from cliptools_app import gui_details_panel
from cliptools_app import gui_shell_panel


class GuiLinesFrame(wx.Frame):

    """Main window with the lines"""

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)

        # Callbacks that will be registered by the Controller
        self.handle_keyboard_events = None
        self.handle_focus_event = None
        self.handle_update_request = None

        # Periodic timer events
        self.update_timer = wx.Timer(self)
        self.update_timer.Start(500)
        self.Bind(wx.EVT_TIMER, self.on_update_timer)

        # Key events are binded to the frame
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

        # Button events are handled by button names, generic handler is enough
        self.Bind(wx.EVT_BUTTON, self.on_button_click)

        # And also use a sizer to manage the size of the panel such
        # that it fills the frame
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_v = wx.BoxSizer(wx.VERTICAL)

        # Create the main panel with the lines
        self.lines_panel = gui_lines_panel.LinesPanel(self)
        sizer_v.Add(self.lines_panel, 0, wx.EXPAND)

        # Create the details panel with the multi-line texts
        self.details_panel = gui_details_panel.DetailsPanel(self)
        sizer_v.Add(self.details_panel, 1, wx.EXPAND)

        sizer_h.Add(sizer_v, 1, wx.EXPAND)

        self.shell_panel = gui_shell_panel.ShellPanel(self)
        sizer_h.Add(self.shell_panel, 1, wx.EXPAND)

        self.SetSizer(sizer_h)
        #self.Layout()
        self.Fit()

    def on_update_timer(self, event):
        """Periodic clipboard check and trigger controller checks"""
        text = gui_tools.get_clip_content()
        self.handle_update_request(text)
        event.Skip()

    def on_key_press(self, event):
        """Function to respond to key press events.
        Number key press will select the actual line
        letters do various tasks.
        Actual tasks delegated to the controller"""
        cmd_txt = ""
        # Modifiers
        for mod, text in [
                (event.ShiftDown(), 'Shift-'),
                (event.ControlDown(), 'Ctrl-'),
                (event.AltDown(), 'Alt-'),
            ]:
            if mod:
                cmd_txt += text
        # Key name
        key_code = event.GetKeyCode()
        key_name = commands.SPECIAL_KEYS.get(key_code, None)
        if key_name is None:
            key_name = chr(key_code)
        cmd_txt += key_name
        # Command sequence string based on modifiers and name
        cmd_seq = commands.KEY_COMMANDS.get(cmd_txt, "")
        for cmd_item in cmd_seq:
            self.handle_keyboard_events(cmd_item)
        event.Skip()

    def on_button_click(self, event):
        """Function to respond to button clicks.
        Number button click will select the actual line
        other buttons handled too.
        Actual tasks delegated to the controller based on button name"""
        btn_name = event.GetEventObject().GetName()
        self.handle_keyboard_events(btn_name)
        event.Skip()

    def update_data(self, title, data_iter, selected_text, action_doc, processed_text, focus_number):
        """Update the line data from the provided generator/iterator
        Beside also update details texts and line focus"""
        self.lines_panel.update_data(title, data_iter, focus_number)
        self.details_panel.update_data(selected_text, action_doc, processed_text)
