"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

By BigBirdCode
https://github.com/bigbirdcode/cliptools
"""

import pathlib
import shutil
import socket
import sys
from typing import Never

import platformdirs

from cliptools.modules.config import read_config


SERVER_SUCCESS = "CLIP-OK."


def error_and_exit(msg: str) -> Never:
    """
    Show an error both on console and on UI then exit.
    """
    from tkinter import messagebox  # pylint: disable=import-outside-toplevel

    messagebox.showerror("System exit", msg)
    print(msg)  # noqa: T201 - print
    sys.exit(1)


def get_or_create_user_folder() -> pathlib.Path:
    """
    Return the user configuration folder or create one when not found.

    If the folder is empty then function will also copy the sample files there.
    To avoid this behavior, leave at least a placeholder file there,
    for example the 'cliptools.txt' file.
    """
    folder = platformdirs.user_data_dir(appname="cliptools", appauthor=False, roaming=True)
    folder_path = pathlib.Path(folder)
    try:
        folder_path.mkdir(parents=True, exist_ok=True)
    except OSError:
        msg = f"Cannot create user folder {folder_path}"
        error_and_exit(msg)
    if not any(folder_path.iterdir()):
        # folder is empty
        samples = pathlib.Path(__file__).parent / "samples"
        assert samples.is_dir(), f"Cannot found samples folder {samples}"
        for f in samples.iterdir():
            shutil.copy(f, folder_path)
    return folder_path


def _try_delegate_to_existing_instance(port: int, args: list[str]) -> socket.socket | bool:
    """
    Try to create server socket.
    This is fastest way to find out if app is already running

    Function taken from Thonny, Python IDE for beginners at https://thonny.org/
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", port))
        server_socket.listen(10)
    except OSError:
        # port was already taken, most likely by previous instance.
        # Try to connect and send arguments
        return _delegate_to_existing_instance(port, args)
    else:
        # we were able to create server socket (ie. app was not running)
        # Let's use the socket in the app
        return server_socket


def _delegate_to_existing_instance(port: int, args: list[str]) -> bool:
    """
    Sending arguments to existing instance
    If an error happen we quit, no fancy messages here
    Return: true - ok; false - ops, we connected something else...

    Function taken from Thonny, Python IDE for beginners at https://thonny.org/
    """
    data = repr(args).encode(encoding="utf_8")
    sock = socket.create_connection(("localhost", port))
    sock.sendall(data)
    sock.shutdown(socket.SHUT_WR)
    response = bytes([])
    while len(response) < len(SERVER_SUCCESS):
        new_data = sock.recv(2)
        if not new_data:
            break
        response += new_data
    return response.decode("UTF-8") == SERVER_SUCCESS


def main() -> None:
    """
    Main function.

    Trying whether there is an existing app, or start a new one
    command line parameters are passed in any way to the running one.
    """
    user_folder = get_or_create_user_folder()
    config = read_config(user_folder)
    if isinstance(config, str):
        error_and_exit(config)

    port = config.port
    delegation_result = _try_delegate_to_existing_instance(port, sys.argv[1:])
    if delegation_result is True:
        # Delegated to an existing instance. Exiting now.
        return
    if hasattr(delegation_result, "accept"):
        # we have server socket to put in use
        server_socket = delegation_result
    else:
        # something bad happened
        msg = "Ops, something bad happened, could not create server socket or we contacted something else..."
        error_and_exit(msg)

    # So far ok, time to load the entire app and start working
    from cliptools.modules import controller  # pylint: disable=import-outside-toplevel

    control = controller.Controller(server_socket, user_folder, config, sys.argv[1:])
    control.start()


if __name__ == "__main__":
    main()
