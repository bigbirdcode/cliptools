=========
ClipTools
=========

Goal
----

Clipboard manager with text processing tools.

Yes, there are many clipboard managers, but I had this idea, how to make it simple and effective. 

Programming language: Python and wxPython.

Test suite: Pytest

Inspiration
-----------

The book Fluent Python by Luciano Ramalho, http://bit.ly/fluentpy inspired me to start some new projects. I especially liked the unicode part, as the examples were really great and solved the problems what I have with the Hungarian language.

Thonny, Python IDE for beginners at https://thonny.org/ has interesting structure. I borrowed the starting part with the delegation handling sockets.

And of course Python and wxPython are great!

Concept
-------

ClipTools clipboard manager is collecting texts and files (as texts) copied to the clipboard.
It shows these collected texts to the user in a GUI interface with lines for the texts.
It can also have collection of other useful texts, that the user can define in a Python file.
Beside texts, it has some text processing actions, like uppercase, lowercase, backslash duplication, getting file content, etc.User can apply these actions on the selected texts and copy the result back to the clipboard.

Assign a keyboard shortcut to the ClipTools app. So you can bring it up just by a key combination. Then you can easily select a group of texts, the actual text, the processing action just by the number keys from 1 to 9. Finally the processed text result is copied to the clipboard and the app is minimized again.

In addition minimal text editing is possible and a Python shell is provided for quick manipulation of texts. But these are basic functionalities, I suggest separate editors for real text editing. But with the clipboard transfers ClipTools can be a great help.

Here is a screenshot, it is so simple:

.. image:: screenshot.png

Status
------

Work has just started, but I think it is already useful. I would say feasibility study was successful. And I'm also learning Github. Please be patient.

:-)

BigBirdCode
