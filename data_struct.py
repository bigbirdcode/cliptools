"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Definition of data structures used to store text and action data
Data structures are implementing an interface.
Right now they are a bit repetitive, will be improved later.
"""

from text_functions import limit_text, safe_action

class TextData:

    """Text data storage structure"""

    def __init__(self, name, content):
        self.name = name
        self.content = list(content)

    def add_content(self, s):
        self.content.insert(0, s)

    def get_content(self, n):
        try:
            return self.content[n]
        except IndexError:
            return self.content[-1]

    def get_names(self):
        """Iterator, returning the context"""
        for name in self.content:
            yield limit_text(name)


class ActionData:

    """Action, i.e. text processing tools data storage structure"""

    def __init__(self, name, content):
        self.name = name
        self.content = list()
        self.actions = dict()
        for k, v in content:
            self.content.append(k)
            self.actions[k] = v

    def add_content(self, name, action):
        if name in self.content:
            raise RuntimeError('Redeclaration of ' + name)
        self.content.append(name)
        self.actions[name] = action

    def get_content(self, n):
        try:
            name = self.content[n]
        except IndexError:
            name = self.content[-1]
        action = self.actions[name]
        return action

    def get_names(self, txt):
        """Iterator, returning the context"""
        for name in self.content:
            action = self.actions[name]
            result = safe_action(txt, action)
            result = limit_text(result)
            result = "{}: {}".format(name, result)
            yield result


class DataCollection:

    """Collection will store multiple data storage instances"""

    def __init__(self):
        self.children = list()

    def add_child(self, child):
        self.children.append(child)

    def get_child(self, n):
        try:
            return self.children[n]
        except IndexError:
            return self.children[-1]

    def get_names(self):
        """Iterator, returning the context"""
        for child in self.children:
            yield child.name


class DataCollections:

    """Collections contain 2 collection elements, altogether representing the 4 levels of data
    self.clip is a special data, it will store clipboard texts"""

    def __init__(self):
        self.clip = TextData("clips", "")

        self.texts = DataCollection()
        self.texts.add_child(self.clip)

        self.actions = DataCollection()
