"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

This is an example text data file, showing how you can add frequently used data.
You can create similar file in your home folder with your personal content.
See EXTERNAL_DATA configuration parameter for details.

WARNING, python file will be executed!
When making personal file, take care not allow uncontrolled changes!

Sample pre-defined text.

Note: logging is not part of ClipTools yet. Only minimalistic feedback is give.
If personal text file not found then tool will silently read the default.
If personal text file load has an error then a print to a console (if available)
is given.
"""

from collections import OrderedDict


# Please use the name DEFINED_TEXTS the same way
# if you are making your own data file
DEFINED_TEXTS = OrderedDict()


# Below you can customize your data

DEFINED_TEXTS["samples"] = [
    "ÁRVÍZTŰRŐ TÜKÖRFÚRÓGÉP",
    "árvíztűrő tükörfúrógép",
    "Öt szép szűzlány őrült írót nyúz.",
]

DEFINED_TEXTS["sniplets"] = [
    "class",
    "def",
    "main",
    ]

DEFINED_TEXTS["my_data"] = [
    "BigBirdCode",
    "Hungary",
    "Budapest",
    ]

DEFINED_TEXTS["some data"] = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
]

DEFINED_TEXTS["lot of data"] = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "40",
    ]
