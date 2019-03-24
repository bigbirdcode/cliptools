"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Text processing actions to list
Note: just a quick implementation for now.
In the future automatic registration is planned.
"""

from collections import OrderedDict

import text_functions
import sanitize


defined_functions = OrderedDict()

defined_functions["paste"] = [
    ("paste", text_functions.identity)
    ]

defined_functions["case"] = [
    ("upper", str.upper),
    ("lower", str.lower),
    ("title", str.title),
    ]

defined_functions["accents"] = [
    ("to hun", text_functions.accents_to_hun),
    ("to en", text_functions.accents_to_en),
    ("remove accents", sanitize.shave_marks),
    ("remove all", sanitize.asciize),
    ]

defined_functions["filenames"] = [
    ("content", text_functions.filename_content),
    ("linux", text_functions.filename_linux),
    ("double", text_functions.filename_double),
    ]
