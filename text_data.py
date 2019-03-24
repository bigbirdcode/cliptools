"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Pre-defined text, where you can add frequently used data
"""

from collections import OrderedDict

defined_texts = OrderedDict()


defined_texts["samples"] = [
    "ÁRVÍZTŰRŐ TÜKÖRFÚRÓGÉP",
    "árvíztűrő tükörfúrógép",
    "Öt szép szűzlány őrült írót nyúz.",
]

defined_texts["sniplets"] = [
    "class",
    "def",
    "main",
    ]

defined_texts["my_data"] = [
    "BigBirdCode",
    "Hungary",
    "Budapest",
    ]
