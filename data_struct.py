"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Definition of data structures used to store text and action data
Data structures are implementing an interface.
Right now they are a bit repetitive, will be improved later.
"""

from functools import wraps

from config import MAX_NUMBER_OF_DATA, NUMBER_OF_ROWS
from utils import limit_text, safe_action


class BaseData:

    """Base of all data storage structure"""

    def __init__(self, name, content):
        self.name = name
        self.content = list(content)
        self.location = 0

    def add_content(self, content, end=True):
        """Add an item to the contents and handle size, location"""
        if end:
            self.content.append(content)
            if len(self.content) > MAX_NUMBER_OF_DATA:
                del self.content[0]
        else:
            self.content.insert(0, content)
            if len(self.content) > MAX_NUMBER_OF_DATA:
                del self.content[-1]
            if self.location != 0 and self.location < len(self.content) - 1:
                self.location += 1

    def page_up(self):
        """Page up in the contents"""
        self.location -= NUMBER_OF_ROWS
        if self.location < 0:
            self.location = 0

    def page_down(self):
        """Page down in the contents"""
        self.location += NUMBER_OF_ROWS
        if self.location >= len(self.content):
            # Paging not possible, set it back
            self.location -= NUMBER_OF_ROWS

    def get_content(self, number):
        """Get the content taking into account the location"""
        return self.content[self.location + number]

    def get_name(self, number, text=""):
        """Get the name to represent the content, default is short version
        text can be used for actions, not used for simple texts"""
        return limit_text(self.get_content(number))

    def get_names(self, text=""):
        """Iterator, returning the context
        text can be used for actions, not used for simple texts"""
        for number in range(NUMBER_OF_ROWS):
            try:
                yield self.get_name(number, text)
            except IndexError:
                break


class TextData(BaseData):

    """Text data storage structure, content is a list of strings"""

    def add_content(self, content):
        """Add an item to the contents and handle size, location
        Note: currently only clip data is growing, and new items go to the start"""
        super().add_content(content, end=False)


class ActionData(BaseData):

    """Action, i.e. text processing tools data storage structure
    Content are (name, action) tuples"""

    def add_content(self, name, action):
        """Add an item to the contents and handle size, location, avoid duplicates"""
        if name in (item[0] for item in self.content):
            raise RuntimeError('Redeclaration of ' + name)
        self.content.append((name, action))

    def get_content(self, number):
        """Get the action from the content taking into account the location"""
        content = super().get_content(number)
        return content[1]

    def get_name(self, number, txt):
        """Get the name to represent the content, here applying the action"""
        content = super().get_content(number)
        name, action = content
        result = safe_action(txt, action)
        result = limit_text(result)
        result = "{}: {}".format(name, result)
        return result


class DataCollection(BaseData):

    """Collection will store multiple data storage instances"""

    def __init__(self, name):
        super().__init__(name, [])

    def get_name(self, number, text=""):
        """Get the name to represent the content, here name of the content"""
        content = super().get_content(number)
        return content.name

    def get_content_by_name(self, name):
        """Find the data structure by the name"""
        for content in self.content:
            if content.name == name:
                return content
        raise RuntimeError("Name not found: " + name)

class DataCollections:

    """Collections contain 2 collection elements, altogether representing the 4 levels of data
    self.clip is a special data, it will store clipboard texts"""

    def __init__(self):
        self.clip = TextData("clips", "")

        self.texts = DataCollection("texts")
        self.texts.add_content(self.clip)

        self.actions = DataCollection("actions")


data_collections = DataCollections()


def register_function(action_func):
    """Decorator, that will store the functions in actions data
    function name should be <dataname>_<functionname>"""
    data_name, func_name = action_func.__name__.split('_', 1)
    try:
        data = data_collections.actions.get_content_by_name(data_name)
    except RuntimeError:
        data = ActionData(data_name, "")
        data_collections.actions.add_content(data)
    @wraps(action_func)
    def wrapper(*args, **kwds):
        return action_func(*args, **kwds)
    data.add_content(func_name, wrapper)
    return wrapper
