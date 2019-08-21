"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

By BigBird who like to Code
https://github.com/bigbirdcode/cliptools
"""

import os
import socket
import sys


# This file is the starting point of the Cliptools app.
# Python has 2 types of calls:
#  - direct call, like: python main.py
#  - package call, like: python -m cliptools
# Below quite ugly code will handle that
if __name__ == '__main__' and __package__ is None:
    # This was a direct call
    # package information is missing, and relative imports will fail
    # this hack imitates the package behavior and add outer dir to the path
    __package__ = "cliptools"  # pylint: disable=redefined-builtin
    cliptools_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if cliptools_dir not in sys.path:
        sys.path.insert(0, cliptools_dir)
    del cliptools_dir # clean up global name space

# Now relative import is ok
from . import config  # pylint: disable=wrong-import-position


def _try_delegate_to_existing_instance(args):
    """Try to create server socket.
    This is fastest way to find out if app is already running

    Function taken from Thonny, Python IDE for beginners at https://thonny.org/
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", config.PORT))
        server_socket.listen(10)
        # we were able to create server socket (ie. app was not running)
        # Let's use the socket in the app
        return server_socket
    except OSError:
        # port was already taken, most likely by previous instance.
        # Try to connect and send arguments
        return _delegate_to_existing_instance(args)


def _delegate_to_existing_instance(args):
    """Sending arguments to existing instance
    If an error happen we quit, no fancy messages here
    Return: true - ok; false - ops, we connected something else...

    Function taken from Thonny, Python IDE for beginners at https://thonny.org/
    """
    data = repr(args).encode(encoding="utf_8")
    sock = socket.create_connection(("localhost", config.PORT))
    sock.sendall(data)
    sock.shutdown(socket.SHUT_WR)
    response = bytes([])
    while len(response) < len(config.SERVER_SUCCESS):
        new_data = sock.recv(2)
        if not new_data:
            break
        else:
            response += new_data
    return response.decode("UTF-8") == config.SERVER_SUCCESS


def main():
    """Main function
    Trying whether there is an existing app, or start a new one
    command line parameters are passed in any way
    """
    delegation_result = _try_delegate_to_existing_instance(sys.argv[1:])
    if delegation_result is True:
        # we're done
        print("Delegated to an existing instance. Exiting now.")
        return
    if hasattr(delegation_result, "accept"):
        # we have server socket to put in use
        server_socket = delegation_result
    else:
        # something bad happened
        from tkinter import messagebox
        msg = "Ops, something bad happened, maybe we contacted something else..."
        messagebox.showerror("System exit", msg)
        print(msg)
        sys.exit(1)

    # So far ok, time to load the entire app and start working
    from .modules import controller

    control = controller.Controller(server_socket, sys.argv[1:])
    control.start()


if __name__ == "__main__":
    main()
