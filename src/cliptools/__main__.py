"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

By BigBird who like to Code
https://github.com/bigbirdcode/cliptools
"""


# This file "__main__.py" is called when calling the app as package
# like python -m cliptools
# Therefore check on __package__ variable is not needed,
# and relative import is ok.
#
# in short, do not call this file directly, call "main.py" instead

if __name__ == "__main__":
    from . import main

    main.main()
