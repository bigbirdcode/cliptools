"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

By BigBird who like to Code
https://github.com/bigbirdcode/cliptools
"""

import os
import socket
import sys

from cliptools import config


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
        from tkinter import messagebox  # pylint: disable=import-outside-toplevel

        msg = "Ops, something bad happened, maybe we contacted something else..."
        messagebox.showerror("System exit", msg)
        print(msg)
        sys.exit(1)

    # So far ok, time to load the entire app and start working
    from cliptools.modules import controller  # pylint: disable=import-outside-toplevel

    control = controller.Controller(server_socket, sys.argv[1:])
    control.start()


if __name__ == "__main__":
    main()
