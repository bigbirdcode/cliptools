"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Definition of data structures used to store text and action data
"""
import pathlib
from collections.abc import Callable, Iterable
from functools import wraps

import strictyaml

from cliptools.modules import utils
from cliptools.modules.config import Config


class BaseData:
    """Base of all data storage structure"""

    def __init__(self, name: str, contents: Iterable[str] | None = None) -> None:
        self.name = name
        if contents:
            # at creation size is not checked
            # user may want to create large data sets
            self.contents = list(contents)
        else:
            self.contents = []
        self.max_number_of_data = 0  # switched off by default
        self.number_of_rows = 9
        self.location = 0  # used for page up-down, where are we
        self.focus = 0  # what is in focus, from 0 to self.config.number_of_rows - 1

    def set_config(self, config: Config, *, need_max: bool = False) -> None:
        """Set instance values from config"""
        self.number_of_rows = config.number_of_rows
        if need_max:
            self.max_number_of_data = config.max_number_of_data
            # TODO: clear data accordingly

    def is_first_selected(self) -> bool:
        """Check whether the first item is selected"""
        return self.location == 0 and self.focus == 0

    def add_content(self, content, end=True):
        """Add an item to the contents and handle size, location"""
        if end:
            self.contents.append(content)
            if self.max_number_of_data and len(self.contents) > self.max_number_of_data:
                del self.contents[0]
        else:
            self.contents.insert(0, content)
            if self.max_number_of_data and len(self.contents) > self.max_number_of_data:
                del self.contents[-1]
            if self.location == 0:
                # if first data is on page, keep it, data moves
                if 0 < self.focus < self.number_of_rows - 1:
                    # if first data is in focus, keep it, data moves
                    # else focus will keep the same data
                    # config.number_of_rows - 1 cannot increase any more
                    self.focus += 1
            else:
                # else page will keep the same data, collecting before existing
                self.location += 1

    def page_up(self):
        """Page up in the contents"""
        if self.location == 0:
            # first page, focus moves
            self.focus = 0
        elif self.location < self.number_of_rows:
            self.location = 0
        else:
            self.location -= self.number_of_rows

    def page_down(self):
        """Page down in the contents"""
        if self.location >= len(self.contents) - self.number_of_rows:
            # at the end, focus last element
            self.focus = len(self.contents) - self.location - 1
        else:
            self.location += self.number_of_rows
            if self.location + self.focus >= len(self.contents):
                self.focus = len(self.contents) - self.location - 1

    def set_focus(self, number):
        """Set the focus to the given line, check available data"""
        if 0 <= number < self.number_of_rows and self.location + number < len(self.contents):
            # no change in focus if out of range
            self.focus = number

    def focus_down(self):
        """Move the focus down, i.e. increase, check handled by set_focus"""
        self.set_focus(self.focus + 1)

    def focus_up(self):
        """Move the focus up, i.e. decrease, check handled by set_focus"""
        self.set_focus(self.focus - 1)

    def get_focused_content(self):
        """Get the content that has the focus"""
        return self.get_content(self.focus)

    def get_content(self, number):
        """Get the content taking into account the location"""
        # Check if line is valid, list index will check content
        if 0 <= number < self.number_of_rows:
            return self.contents[self.location + number]
        raise IndexError()

    def get_name(self, number, text=""):
        """
        Get the name to represent the content, default is short version

        text can be used for actions, not used for simple texts
        """
        return utils.limit_text(self.get_content(number))

    def get_names(self, text=""):
        """
        Iterator, returning the context. Return empty strings if not enough data.

        Parameter text can be used for actions, not used for simple texts
        """
        for number in range(self.number_of_rows):
            try:
                yield self.get_name(number, text)
            except IndexError:
                yield ""


class TextData(BaseData):
    """Text data storage structure, content is a list of strings"""

    def add_content(self, content, end=False):
        """
        Add an item to the contents and handle size, location

        Note: currently only clip data is growing, and new items go to the start
        """
        super().add_content(content, end=end)


class ActionData(BaseData):
    """
    Action, i.e. text processing tools data storage structure

    Content are (name, action) tuples
    """

    def add_content(self, content, end=True):
        """Add an item to the contents and handle size, location, avoid duplicates"""
        name, action = content  # pylint: disable=unused-variable
        if name in (item[0] for item in self.contents):
            raise RuntimeError("Redeclaration of " + name)
        super().add_content(content, end=end)

    def get_content(self, number):
        """Get the action from the content taking into account the location"""
        content = super().get_content(number)
        return content[1]

    def get_name(self, number, text=""):
        """Get the name to represent the content, here applying the action"""
        content = super().get_content(number)
        name, action = content
        result = utils.safe_action(text, action)
        result = utils.limit_text(result)
        result = f"{name}: {result}"
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
    """
    Collections contain 2 collection elements, altogether representing the 4 levels of data

    self.clip is a special data, it will store clipboard texts
    self.actions is also special, feed by the register_function decorator
    """

    def __init__(self) -> None:
        self.clip = TextData("clips", [""])

        self.texts = DataCollection("text groups")
        self.texts.add_content(self.clip)

        self.actions = _action_collection

    def set_config(self, config: Config) -> None:
        """Set a config to all collections"""
        for text_collection in self.texts.contents:
            text_collection.set_config(config)
        for action_collection in self.actions.contents:
            action_collection.set_config(config)
        self.clip.set_config(config, need_max=True)

    def load_data(self, user_folder: pathlib.Path) -> None:
        """Load available personal or sample text data"""
        for f in user_folder.glob("*.yml"):
            if f.name == "config.yml":
                continue
            content = f.read_text(encoding="utf-8")
            new_data = strictyaml.load(content).data
            for name, data_part in new_data.items():
                self.texts.add_content(TextData(name, data_part))


# data collection instance to hold action data
# defined here at module level so decorator can refer to it
_action_collection = DataCollection("action groups")


def register_function(action_func: Callable[[str], str]) -> Callable[[str], str]:
    """
    Decorator, that will store the functions in actions data.

    function name should be <dataname>_<functionname>
    """
    data_name, func_name = action_func.__name__.split("_", 1)
    try:
        data = _action_collection.get_content_by_name(data_name)
    except RuntimeError:
        data = ActionData(data_name, None)
        _action_collection.add_content(data)

    @wraps(action_func)
    def wrapper(*args, **kwds):
        return action_func(*args, **kwds)

    content = (func_name, wrapper)
    data.add_content(content)
    return wrapper


@register_function
def paste_paste(text: str) -> str:
    """
    Dummy function, return the same text

    >>> paste_paste('foo')
    'foo'
    """
    return text
