"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Controller part, driving the GUI and the Data
"""

import ast
import queue
import socket
import sys
from threading import Thread

import data_struct
import gui_lines
import text_data
import action_data
from config import SERVER_SUCCESS
from text_functions import safe_action

# states
TEXTS = 1
TEXT = 2
ACTIONS = 3
ACTION = 4
MINIMIZED = 5


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


class Controller:

    """Controller class, driving the GUI and the Data"""

    def __init__(self, server_socket, init_args):
        self.server_socket = server_socket
        self.server_queue = queue.Queue()
        for item in init_args:
            self.server_queue.put(item)
        self.last_clip = ""

        self.data = data_struct.DataCollections()
        self.load_data()
        self.app = gui_lines.GuiLinesApp()
        self.app.register_callbacks(self.handle_keyboard_events, self.handle_update_request)

        self.step = TEXTS
        self.actual = self.data.texts
        self.selected_text_data = None
        self.selected_text = None
        self.selected_action_data = None
        self.selected_action = None

    def start(self):
        """Start the thread for delegation check and the mainloop of the GUI"""
        _init_server_loop(self.server_socket, self.server_queue)
        self.update_app()
        self.app.MainLoop()

    def handle_keyboard_events(self, key):
        """Function to handle commands, main source are GUI keyboard events
        but in the future it will handle command line commands too"""
        if key in "123456789":
            n = int(key) - 1
            self.get_next(n)
        else:
            self.get_prev()
        self.update_app()

    def handle_update_request(self, text):
        """Function to handle texts coming from the clipboard and checking delegation requests
        Right now GUI mainloop is checking periodically the clipboard.
        This function is then called.
        It was easier to handle delegation checks here too.
        May have a better implementation in the future."""
        if text and text != self.last_clip:
            self.data.clip.add_content(text)
            self.last_clip = text
            if self.step == TEXT:
                self.update_app()
        while not self.server_queue.empty():
            cmd = self.server_queue.get_nowait()
            # TODO: In the future sequence of commands can be processed
            if cmd == "1":
                if self.step == MINIMIZED:
                    self.step = TEXT
                self.app.bring_to_front()
                self.update_app()
            elif cmd == "0":
                sys.exit(0)

    def update_app(self):
        """Function to push updates to GUI
        sources can be keyboard events, delegation requests or clipboard changes"""
        if self.step == TEXTS:
            self.app.frame.update_data(self.data.texts.get_names())
        elif self.step == TEXT:
            self.app.frame.update_data(self.selected_text_data.get_names())
        elif self.step == ACTIONS:
            self.app.frame.update_data(self.data.actions.get_names())
        elif self.step == ACTION:
            self.app.frame.update_data(self.selected_action_data.get_names(self.selected_text))
        elif self.step == MINIMIZED:
            pass

    def get_next(self, n):
        if self.step == TEXTS:
            self.selected_text_data = self.data.texts.get_child(n)
            self.step = TEXT
        elif self.step == TEXT:
            self.selected_text = self.selected_text_data.get_content(n)
            self.step = ACTIONS
        elif self.step == ACTIONS:
            self.selected_action_data = self.data.actions.get_child(n)
            self.step = ACTION
        elif self.step == ACTION:
            self.selected_action = self.selected_action_data.get_content(n)
            self.step = MINIMIZED
            gui_lines.set_clip_content(safe_action(self.selected_text, self.selected_action))
            self.app.minimize()
        elif self. step == MINIMIZED:
            pass

    def get_prev(self):
        if self.step == ACTION:
            self.step = ACTIONS
        elif self.step == ACTIONS:
            self.step = TEXT
        elif self.step == TEXT:
            self.step = TEXTS
        elif self.step == TEXTS or self.step == MINIMIZED:
            pass

    def load_data(self):
        for name, data in text_data.defined_texts.items():
            self.data.texts.add_child(data_struct.TextData(name, data))
        for name, data in action_data.defined_functions.items():
            self.data.actions.add_child(data_struct.ActionData(name, data))
