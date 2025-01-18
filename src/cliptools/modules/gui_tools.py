"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Tools and utilities related to the wx module
"""

import wx
import wx.adv


def show_info():
    """Display program info"""
    with open("LICENSE.txt") as f:
        license_text = f.read()
    info = wx.adv.AboutDialogInfo()
    info.Name = "cliptools"
    info.Version = "1.0"
    info.Copyright = "(c) 2019-2019 BigBirdCode"
    info.Description = str(
        '"ClipTools" is a clipboard manager with text processing tools.\n\n'
        "App is listening to keyboard and collecting texts copied to the clipboard. It can\n"
        "also have collection of other useful texts. Beside texts, it has some actions, like\n"
        "uppercase, lowercase, backslash duplication, getting file content, etc.\n\n"
        "You can assign a keyboard shortcut to the ClipTools app. So it can be started by\n"
        "just a key combination. Then you can easily select a group of texts, the actual\n"
        "text, the processing action just by the number keys from 1 to 9. Finally the\n"
        "processed text result is copied to the clipboard."
    )
    info.WebSite = ("https://github.com/bigbirdcode/cliptools", "ClipTools Github page")
    info.Developers = ["BigBirdCode"]
    info.License = license_text
    # Then we call wx.AboutBox giving it that info object
    wx.adv.AboutBox(info)


def show_error(msg):
    """Error message to show"""
    dlg = wx.MessageDialog(None, msg, "ClipTools", wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    dlg.Destroy()


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
            # print("Unable to open the clipboard")
            return ""
    except Exception:  # pylint: disable=broad-except
        # print("Unable to open the clipboard")
        return ""
    if success_text:
        return tdo_text.GetText()
    if success_file:
        return "\n".join(tdo_file.GetFilenames())
    return ""


def set_clip_content(text):
    """Copy a processed text to the clipboard"""
    tdo = wx.TextDataObject()
    tdo.SetText(text)
    if wx.TheClipboard.Open():
        wx.TheClipboard.SetData(tdo)
        wx.TheClipboard.Close()
    else:
        show_error("Unable to open the clipboard, try again.")
