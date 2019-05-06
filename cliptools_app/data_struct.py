"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Definition of data structures used to store text and action data
"""

from functools import wraps

from config import MAX_NUMBER_OF_DATA, NUMBER_OF_ROWS
from cliptools_app.utils import limit_text, safe_action


class BaseData:

    """Base of all data storage structure"""

    def __init__(self, name, contents=None):
        self.name = name
        if contents:
            # at creation size is not checked
            # user may want to create large data sets
            self.contents = list(contents)
        else:
            self.contents = list()
        self.location = 0

    def add_content(self, content, end=True):
        """Add an item to the contents and handle size, location"""
        if end:
            self.contents.append(content)
            if len(self.contents) > MAX_NUMBER_OF_DATA:
                del self.contents[0]
        else:
            self.contents.insert(0, content)
            if len(self.contents) > MAX_NUMBER_OF_DATA:
                del self.contents[-1]
            if self.location != 0 and self.location < len(self.contents) - 1:
                self.location += 1

    def page_up(self):
        """Page up in the contents"""
        self.location -= NUMBER_OF_ROWS
        if self.location < 0:
            self.location = 0

    def page_down(self):
        """Page down in the contents"""
        self.location += NUMBER_OF_ROWS
        if self.location >= len(self.contents):
            # Paging not possible, set it back
            self.location -= NUMBER_OF_ROWS

    def get_content(self, number):
        """Get the content taking into account the location"""
        if number >= NUMBER_OF_ROWS:
            raise IndexError()
        return self.contents[self.location + number]

    def get_name(self, number, text=""):  # pylint: disable=unused-argument
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

    def add_content(self, content, end=None):
        """Add an item to the contents and handle size, location
        Note: currently only clip data is growing, and new items go to the start"""
        if end is None:
            end = False
        super().add_content(content, end=end)


class ActionData(BaseData):

    """Action, i.e. text processing tools data storage structure
    Content are (name, action) tuples

    Note: assuming that items are added one by one,
    init not checking duplicates
    """

    def add_content(self, content, end=True):
        """Add an item to the contents and handle size, location, avoid duplicates"""
        name, action = content  # pylint: disable=unused-variable
        if name in (item[0] for item in self.contents):
            raise RuntimeError('Redeclaration of ' + name)
        super().add_content(content, end=end)

    def get_content(self, number):
        """Get the action from the content taking into account the location"""
        content = super().get_content(number)
        return content[1]

    def get_name(self, number, text=""):
        """Get the name to represent the content, here applying the action"""
        content = super().get_content(number)
        name, action = content
        result = safe_action(text, action)
        result = limit_text(result)
        result = "{}: {}".format(name, result)
        return result


class DataCollection(BaseData):

    """Collection will store multiple data storage instances"""

    def get_name(self, number, text=""):
        """Get the name to represent the content, here name of the content"""
        content = super().get_content(number)
        return content.name

    def get_content_by_name(self, name):
        """Find the data structure by the name"""
        for content in self.contents:
            if content.name == name:
                return content
        raise RuntimeError("Name not found: " + name)


class DataCollections:

    """Collections contain 2 collection elements, altogether representing the 4 levels of data
    self.clip is a special data, it will store clipboard texts"""

    def __init__(self):
        self.clip = TextData("clips", "")

        self.texts = DataCollection("text groups")
        self.texts.add_content(self.clip)

        self.actions = DataCollection("action groups")


data_collections = DataCollections()


def register_function(action_func):
    """Decorator, that will store the functions in actions data
    function name should be <dataname>_<functionname>"""
    data_name, func_name = action_func.__name__.split('_', 1)
    try:
        data = data_collections.actions.get_content_by_name(data_name)
    except RuntimeError:
        data = ActionData(data_name, None)
        data_collections.actions.add_content(data)
    @wraps(action_func)
    def wrapper(*args, **kwds):
        return action_func(*args, **kwds)
    content = (func_name, wrapper)
    data.add_content(content)
    return wrapper
