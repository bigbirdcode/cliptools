"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Main frame of the GUI App. It will contains the lines, the details and the shell panels
"""

import os

import wx

from . import commands
from . import gui_tools
from . import gui_lines_panel
from . import gui_details_panel
from . import gui_shell_panel


class GuiLinesFrame(wx.Frame):

    """Main frame with the lines, details, shell"""

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)

        # Callbacks that will be registered by the Controller
        self.handle_keyboard_events = None
        self.handle_focus_event = None
        self.handle_new_text = None
        self.handle_update_request = None

        # Colors to use for the lines
        self.active_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_ACTIVECAPTION)
        self.normal_color = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)

        # Icon
        iconfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources', 'cliptools.png')
        icon = wx.Icon(iconfile, wx.BITMAP_TYPE_ANY)
        self.SetIcon(icon)

        # Periodic timer events
        self.update_timer = wx.Timer(self)
        self.update_timer.Start(500)
        self.Bind(wx.EVT_TIMER, self.on_update_timer)

        # Key events are binded to the frame
        self.edit_mode = False
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

        # Button events are handled by button names, generic handler is enough
        self.Bind(wx.EVT_BUTTON, self.on_button_click)

        # And also use a sizer to manage the size of the panel such lines,
        # details, shell that it fills the frame
        sizer_h = wx.BoxSizer(wx.HORIZONTAL)
        sizer_v = wx.BoxSizer(wx.VERTICAL)

        # Create the main panel with the lines
        self.lines_panel = gui_lines_panel.LinesPanel(self)
        sizer_v.Add(self.lines_panel, 0, wx.EXPAND)

        # Create the details panel with the multi-line texts
        self.details_panel = gui_details_panel.DetailsPanel(self)
        sizer_v.Add(self.details_panel, 0, wx.EXPAND)

        sizer_h.Add(sizer_v, 0, wx.EXPAND)

        # Create the shell panel
        self.shell_panel = gui_shell_panel.ShellPanel(self)
        sizer_h.Add(self.shell_panel, 1, wx.EXPAND)

        # Set and fit everything
        self.SetSizer(sizer_h)
        self.Layout()
        self.Fit()

    def register_callbacks(self,
                           handle_keyboard_events,
                           handle_focus_event,
                           handle_new_text,
                           handle_update_request):
        """Callbacks coming from controller to handle communication"""
        self.handle_keyboard_events = handle_keyboard_events
        self.handle_focus_event = handle_focus_event
        self.handle_new_text = handle_new_text
        self.handle_update_request = handle_update_request

    def on_update_timer(self, event):
        """Periodic clipboard check and trigger controller checks"""
        text = gui_tools.get_clip_content()
        self.handle_update_request(text)
        event.Skip()

    def on_key_press(self, event):
        """Function to respond to key press events.
        Number key press will select the actual line.
        Letters do various tasks.
        Actual tasks delegated to the controller"""
        if self.edit_mode:
            # editor will handle the key-press
            event.Skip()
            return
        # Build command string based on modifiers and name
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
        # Check whether it is a valid key
        try:
            cmd_seq = commands.KEY_COMMANDS[cmd_txt]
        except KeyError:
            # cannot handle
            event.Skip()
            return
        for cmd_item in cmd_seq:
            self.handle_keyboard_events(cmd_item)
        #event.Skip()

    def on_button_click(self, event):
        """Function to respond to button clicks.
        Button names define the actions as keys.
        Number button click will select the actual line.
        Other buttons do various tasks.
        Actual tasks delegated to the controller based on button name"""
        btn_name = event.GetEventObject().GetName()
        self.handle_keyboard_events(btn_name)
        event.Skip()

    def update_data(self, title, data_iter, focus_number, selected_text, action_doc, processed_text):
        """Update the line data from the provided generator/iterator
        Beside also update details texts and line focus"""
        self.lines_panel.update_data(title, data_iter, focus_number)
        self.details_panel.update_data(selected_text, action_doc, processed_text)
