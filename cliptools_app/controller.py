"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Controller part, driving the GUI and the Data
"""

import ast
import queue
import socket
from threading import Thread

from cliptools_app import commands
from cliptools_app import data_struct
from cliptools_app import gui_app
from cliptools_app import gui_tools
from cliptools_app import text_functions  # pylint: disable=unused-import
from cliptools_app.utils import safe_action

from config import SERVER_SUCCESS

# states of the app
TEXTS = 1
TEXT = 2
ACTIONS = 3
ACTION = 4


###########################################################
#
# Internal server functions to handle commands
#
###########################################################


def _handle_socket_request(client_socket, server_queue) -> None:
    """handle each connection, runs in separate thread"""
    # read the request
    data = bytes()
    while True:
        new_data = client_socket.recv(64)
        if new_data:
            data += new_data
        else:
            break
    args = ast.literal_eval(data.decode("UTF-8"))
    if not isinstance(args, list):
        print("Wrong data received through the socket, dropping it.")
        return
    for item in args:
        server_queue.put(item)
    # respond OK
    client_socket.sendall(SERVER_SUCCESS.encode(encoding="utf-8"))
    client_socket.shutdown(socket.SHUT_WR)


def _init_server_loop(server_socket, server_queue) -> None:
    """Socket will listen requests from newer instances,
    which try to delegate commands to older instance
    """

    def server_loop():
        while True:
            (client_socket, _) = server_socket.accept()
            _handle_socket_request(client_socket, server_queue)

    Thread(target=server_loop, daemon=True).start()


###########################################################
#
# The Controller class
#
###########################################################


class Controller:

    """Controller class, driving the GUI and the Data"""

    def __init__(self, server_socket, init_args):
        self.server_socket = server_socket
        self.server_queue = queue.Queue()
        for item in init_args:
            self.server_queue.put(item)
        self.last_clip = ""

        self.data = data_struct.data_collections
        self.load_data()
        self.app = gui_app.GuiLinesApp()
        self.app.register_callbacks(self.handle_keyboard_events,
                                    self.handle_focus_event,
                                    self.handle_update_request)

        self.step = TEXTS
        self.actual = self.data.texts
        self.selected_text_data = None
        self.selected_text = ""  # default text is empty text
        self.selected_action_data = None
        self.selected_action = text_functions.paste_paste
        self.processed_text = ""
        self.text_to_clipboard = ""
        self.focus_number = {TEXTS: 0, TEXT: 0, ACTIONS: 0, ACTION: 0}
        self.keyboard_commands = {
            '0': self.app.minimize,
            'A': self.command_backward,
            'D': self.command_forward,
            'W': self.command_focus_up,
            'S': self.command_focus_down,
            'E': self.command_page_down,
            'Q': self.command_page_up,
            'F': self.app.bring_to_front,
            'C': self.command_copy_selected_text,
            'V': self.command_copy_processed_text,
            'I': gui_tools.show_info,
            'Z': self.app.show_hide_details_panel,
            'T': self.command_test
        }

    def start(self):
        """Start the thread for delegation check and the mainloop of the GUI"""
        _init_server_loop(self.server_socket, self.server_queue)
        self.update_app()
        self.app.MainLoop()

    def load_data(self):
        """Load text and action data from the current implementation"""
        try:
            import text_data
        except ImportError:
            return
        for name, data in text_data.DEFINED_TEXTS.items():
            self.data.texts.add_content(data_struct.TextData(name, data))

    ###########################################################
    # Handlers are callbacks, GUI app will call them
    ###########################################################

    def handle_keyboard_events(self, key):
        """Function to handle commands, main source are GUI keyboard events
        but it handles command line commands too"""
        if key in commands.NUM_KEYS:
            number = int(key) - 1
            try:
                self.get_next(number)
                self.get_focus(self.focus_number[self.step])
            except IndexError:
                return  # not valid number, just ignore
        else:
            if key in self.keyboard_commands:
                self.keyboard_commands[key]()  # call the command
            else:
                return  # unknown character, just ignore
        self.update_app()

    def handle_focus_event(self, num_text):
        """Function to handle focus changes on the GUI
        it is a helper for the user to show the details of selected items"""
        try:
            number = int(num_text) - 1
            self.get_focus(number)
        except (ValueError, IndexError):
            return  # not a valid number, return
        self.update_app()

    def handle_update_request(self, text):
        """Function to handle texts coming from the clipboard and checking delegation requests
        Right now GUI mainloop is checking periodically the clipboard.
        This function is then called.
        It was easier to handle delegation checks here too.
        May have a better implementation in the future."""
        if text and text != self.last_clip and text != self.text_to_clipboard:
            self.data.clip.add_content(text)
            self.last_clip = text
            if self.step == TEXT:
                self.update_app()
        while not self.server_queue.empty():
            cmd = self.server_queue.get_nowait()
            self.handle_keyboard_events(cmd)

    ###########################################################
    # Update is pushing the data to the GUI
    ###########################################################

    def update_app(self):
        """Function to push updates to GUI
        sources can be keyboard events, delegation requests or clipboard changes"""
        title = "Select from " + self.actual.name
        self.app.frame.update_data(title,
                                   self.actual.get_names(self.selected_text),
                                   self.selected_text,
                                   self.selected_action.__doc__,
                                   self.processed_text,
                                   self.focus_number[self.step])

    ###########################################################
    # Functions to modify the states of the controller and data
    ###########################################################

    def get_focus(self, number):
        """Set the focus to the n-th item
        If number is out of possible range this will raise IndexError
        It will also process the selected texts"""
        item = self.actual.get_content(number)
        self.focus_number[self.step] = number
        if self.step == TEXTS:
            pass
        elif self.step == TEXT:
            self.selected_text = item
        elif self.step == ACTIONS:
            pass
        elif self.step == ACTION:
            self.selected_action = item
        self.get_processed()

    def get_next(self, number):
        """Step to the next state, select the n-th item for that
        If number is out of possible range this will raise IndexError
        Usually get_focus should follow this function to finish the updates"""
        item = self.actual.get_content(number)
        self.focus_number[self.step] = number
        if self.step == TEXTS:
            self.selected_text_data = item
            self.actual = self.selected_text_data
            self.step = TEXT
        elif self.step == TEXT:
            self.selected_text = item
            self.actual = self.data.actions
            self.step = ACTIONS
        elif self.step == ACTIONS:
            self.selected_action_data = item
            self.actual = self.selected_action_data
            self.step = ACTION
        elif self.step == ACTION:
            self.selected_action = item
            self.actual = self.selected_text_data  # go back to selected text collection
            self.step = TEXT
            self.get_processed()  # extra processing before copying
            self.text_to_clipboard = self.processed_text
            gui_tools.set_clip_content(self.processed_text)
            self.app.minimize()

    def get_processed(self):
        """Update processed text"""
        self.processed_text = safe_action(self.selected_text, self.selected_action)

    def get_prev(self):
        """Step back one state
        Usually get_focus should follow this function to finish the updates"""
        if self.step == ACTION:
            self.actual = self.data.actions
            self.step = ACTIONS
        elif self.step == ACTIONS:
            self.actual = self.selected_text_data
            self.step = TEXT
        elif self.step == TEXT:
            self.actual = self.data.texts
            self.step = TEXTS
        elif self.step == TEXTS:
            pass  # cannot go back from texts state

    ###########################################################
    # Commands contain the details of user commands
    ###########################################################

    def command_focus_down(self):
        """Action to select the next item, move the focus down"""
        number = self.focus_number[self.step] + 1
        try:
            self.get_focus(number)
        except IndexError:
            return  # not a valid number, return

    def command_focus_up(self):
        """Action to select the previous item, move the focus up"""
        number = self.focus_number[self.step] - 1
        try:
            self.get_focus(number)
        except IndexError:
            return  # not a valid number, return

    def command_page_up(self):
        """Action to page up in the list"""
        self.actual.page_up()

    def command_page_down(self):
        """Action to page up in the list"""
        self.actual.page_down()

    def command_backward(self):
        """Go backward, go to the previous state"""
        try:
            self.get_prev()
            self.get_focus(self.focus_number[self.step])
        except IndexError:
            return  # not possible, but better to handle it

    def command_forward(self):
        """Go forward, use the actual selection and go to the next state"""
        try:
            self.get_next(self.focus_number[self.step])
            self.get_focus(self.focus_number[self.step])
        except IndexError:
            return  # not possible, but better to handle it

    def command_copy_selected_text(self):
        """Action to copy the text and minimize"""
        self.text_to_clipboard = self.selected_text
        gui_tools.set_clip_content(self.selected_text)
        self.actual = self.selected_text_data  # go back to selected text collection
        self.step = TEXT
        self.app.minimize()

    def command_copy_processed_text(self):
        """Action to copy the text and minimize"""
        self.text_to_clipboard = self.processed_text
        gui_tools.set_clip_content(self.processed_text)
        self.actual = self.selected_text_data  # go back to selected text collection
        self.step = TEXT
        self.app.minimize()

    def command_test(self):
        """Action to perform something to test & debug"""
        gui_tools.show_error('Test message')
