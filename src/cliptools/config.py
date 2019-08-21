"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Constants, configurations and shared info
"""

# Port number used for inter process communication
# only localhost is allowed, no external connections
PORT = 5555

# Internal message for identification
SERVER_SUCCESS = "CLIP-OK."

# Number of rows in the GUI, should be between 1 and 9, but maybe 9 is the best
# Note: if you change NUMBER_OF_ROWS value change commands accordingly
NUMBER_OF_ROWS = 9

# Number of clipboard history to store
MAX_NUMBER_OF_DATA = 50

# Displayed string length, longer strings truncated to display
STRING_LENTH = 30
