"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Module contain the GUI codes and clipboard polling function
as part of the wx mainloop
"""

from itertools import chain, repeat

import wx
import wx.adv

from cliptools_app import commands
from config import NUMBER_OF_ROWS


def get_clip_content():
    """Checking clipboard content, return text is available"""
    success_text = False
    success_file = False
    tdo_text = wx.TextDataObject()
    tdo_file = wx.FileDataObject()
    try:
        if wx.TheClipboard.Open():
            success_text = wx.TheClipboard.GetData(tdo_text)
            if not success_text:
                success_file = wx.TheClipboard.GetData(tdo_file)
            wx.TheClipboard.Close()
        else:
            print("Unable to open the clipboard")
            return ""
    except Exception:
        print("Unable to open the clipboard")
        return ""
    if success_text:
        return tdo_text.GetText()
    elif success_file:
        return "\n".join(tdo_file.GetFilenames())
    else:
        #print("No clip data in text")
        return ""


def set_clip_content(text):
    """Copy a processed text to the clipboard"""
    tdo = wx.TextDataObject()
    tdo.SetText(text)
    if wx.TheClipboard.Open():
        wx.TheClipboard.SetData(tdo)
        wx.TheClipboard.Close()
    else:
        print("Unable to open the clipboard")


class GuiLinesApp(wx.App):

    """Main GUI App"""

    def OnInit(self):
        """wxPython calls OnInit to create widgets"""
        self.frame = GuiLinesFrame(None, "Clip Tools")
        self.SetTopWindow(self.frame)
        self.frame.Show(True)
        return True

    def register_callbacks(self, handle_keyboard_events, handle_update_request):
        """Callbacks coming from controller to handle communication"""
        self.frame.handle_keyboard_events = handle_keyboard_events
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


class GuiLinesFrame(wx.Frame):

    """Main window with the lines"""

    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)

        # Callbacks that will be registered by the Controller
        self.handle_keyboard_events = None
        self.handle_update_request = None

        # List of textboxes for easier reference
        self.texts = list()

        # Key events are binded to the frame
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

        # Periodic timer events
        self.update_timer = wx.Timer(self)
        self.update_timer.Start(500)
        self.Bind(wx.EVT_TIMER, self.on_update_timer)

        # Now create the Panel to put the other controls on.
        panel = wx.Panel(self)
        # Use a sizer to layout the controls, stacked vertically and with
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Buttons, right now just placeholders
        subsizer = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(panel, -1, "←", size=(25, 25))
        self.Bind(wx.EVT_BUTTON, self.on_button_click, btn)
        subsizer.Add(btn, 0, wx.CENTER)
        self.title_btn = wx.Button(panel, -1, "Title", size=(25, 25))
        self.Bind(wx.EVT_BUTTON, self.on_title_click, self.title_btn)
        subsizer.Add(self.title_btn, 1, wx.CENTER)
        btn = wx.Button(panel, -1, "▲", size=(25, 25))
        self.Bind(wx.EVT_BUTTON, self.on_button_click, btn)
        subsizer.Add(btn, 0, wx.CENTER)
        btn = wx.Button(panel, -1, "▼", size=(25, 25))
        self.Bind(wx.EVT_BUTTON, self.on_button_click, btn)
        subsizer.Add(btn, 0, wx.CENTER)
        sizer.Add(subsizer, 0, wx.EXPAND)

        # Add the lines: 1 button 1 text
        # Use a sizer to layout the controls,
        # stacked vertically and horizontally
        # and with a 10 pixel border around each
        for i in range(NUMBER_OF_ROWS):
            subsizer = wx.BoxSizer(wx.HORIZONTAL)
            btn = wx.Button(panel, -1, str(i+1), size=(25, 25))
            self.Bind(wx.EVT_BUTTON, self.on_button_click, btn)
            subsizer.Add(btn, 0, wx.CENTER)
            text = wx.TextCtrl(panel, -1, "", size=(200, -1))
            subsizer.Add(text, 1, wx.EXPAND)
            sizer.Add(subsizer, 0, wx.EXPAND)
            self.texts.append(text)

        panel.SetSizer(sizer)
        panel.Layout()

        # And also use a sizer to manage the size of the panel such
        # that it fills the frame
        sizer = wx.BoxSizer()
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()

    def on_key_press(self, event):
        """Number key press will select the actual line
        but with delegating the action to the controller"""
        cmd_txt = ""
        # Modifiers
        for mod, text in [
                (event.ShiftDown(),   'Shift-'),
                (event.ControlDown(), 'Ctrl-'),
                (event.AltDown(),     'Alt-'),
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
        """Button click will select the actual line
        but with delegating the action to the controller"""
        btn_text = event.GetEventObject().GetLabel()
        btn_code = btn_text.translate(commands.BUTTON_CODES)
        self.handle_keyboard_events(btn_code)
        event.Skip()

    def on_update_timer(self, event):
        """Periodic clipboard check and trigger controller checks"""
        text = get_clip_content()
        self.handle_update_request(text)

    def update_data(self, title, data_iter):
        """Update the line data from the provided generator/iterator"""
        self.title_btn.SetLabel(title)
        for i, text in enumerate(chain(data_iter, repeat(""))):
            if i >= NUMBER_OF_ROWS:
                break
            entry = self.texts[i]
            entry.Clear()
            entry.AppendText(text)
            entry.SetInsertionPoint(0)

    def on_title_click(self, event):
        """Display program info"""
        with open("LICENSE") as f:
            license_text = f.read()
        info = wx.adv.AboutDialogInfo()
        info.Name = "ClipTools"
        info.Version = "0.2"
        info.Copyright = "(c) 2019-2019 BigBirdCode"
        info.Description = str(
            "\"ClipTools\" is a clipboard manager with text processing tools.\n\n"
            "App is listening to keyboard and collecting texts copied to the clipboard. It can\n"
            "also have collection of other useful texts. Beside texts, it has some actions, like\n"
            "uppercase, lowercase, backslash duplication, getting file content, etc.\n\n"
            "You can assign a keyboard shortcut to the ClipTools app. So it can be started by\n"
            "just a key combination. Then you can easily select a group of texts, the actual\n"
            "text, the processing action just by the number keys from 1 to 9. Finally the\n"
            "processed text result is copied to the clipboard.")
        info.WebSite = ("https://github.com/bigbirdcode/cliptools", "ClipTools Github page")
        info.Developers = ["BigBirdCode"]
        info.License = license_text
        # Then we call wx.AboutBox giving it that info object
        wx.adv.AboutBox(info)
