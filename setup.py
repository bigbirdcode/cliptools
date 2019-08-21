import io
import re

from setuptools import find_packages
from setuptools import setup

long_description = """
ClipTools clipboard manager is collecting texts and files (as texts) copied to the clipboard.
It shows these collected texts to the user in a GUI interface with lines for the texts.
It can also have collection of other useful texts, that the user can define in a Python file.
Beside texts, it has some text processing actions, like uppercase, lowercase, backslash
duplication, getting file content, etc.User can apply these actions on the selected texts
and copy the result back to the clipboard.

Assign a keyboard shortcut to the ClipTools app. So you can bring it up just by a key
combination. Then you can easily select a group of texts, the actual text, the processing
action just by the number keys from 1 to 9. Finally the processed text result is copied to
the clipboard and the app is minimized again.

In addition minimal text editing is possible and a Python shell is provided for quick
manipulation of texts. But these are basic functionalities, I suggest separate editors
for real text editing. But with the clipboard transfers ClipTools can be a great help.
"""

setup(
    name="cliptools",
    version="1.0",
    url="https://github.com/bigbirdcode/cliptools",
    license="MIT License",
    author="BigBirdCode",
    author_email="na",
    description="ClipTools clipboard manager and text processing tools with a lines based GUI interface.",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Desktop Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        'cliptools': ['resources/cliptools.png'],
    },
    python_requires=">=3.5",
    install_requires=[
        "wxPython>=4.0",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pylint",
        ],
    },
    entry_points={"gui_scripts": ["cliptools = cliptools.main:main"]},
)
