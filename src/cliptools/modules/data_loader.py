"""ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Data loader, search for available personal data.

WARNING, python file will be executed!
When making python personal file, take care not allow uncontrolled changes!
yaml is safer from this point of view.

Note: logging is not part of ClipTools yet. Only minimalistic feedback is give.
If personal txt file not found then tool will silently read the default.
If file load has an error then a print to a console (if available) is given.
"""

import pathlib

from .. import config


def load_data():
    """Load available personal or sample text data
    data is an OrderedDict or similar structure,
    where keys are the names, values are list of texts.
    """
    ext_data = pathlib.Path(config.EXTERNAL_DATA)
    if not ext_data.is_absolute():
        ext_data = pathlib.Path.home() / ext_data
    if ext_data.exists():
        try:
            return load_ext_data(ext_data)
        except Exception as exc:  # pylint: disable=broad-except
            # fallback to sample data
            print("Cannot load: {}, exception: {}".format(config.EXTERNAL_DATA, exc))
    return load_sample_data()


def load_ext_data(ext_data):
    """Load external data, raise exception if something is not ok."""
    if ext_data.suffix.lower() == ".py":
        return load_ext_py_data(ext_data)
    if ext_data.suffix.lower() == ".yml":
        return load_ext_yml_data(ext_data)
    raise RuntimeError("Type not supported")


def load_ext_py_data(ext_data):
    """Load external python data.
    WARNING, python file will be executed, take care not allow uncontrolled changes!
    raise exception if something is not ok."""
    content = ext_data.read_text(encoding="utf-8")
    glo = dict()
    loc = dict()
    exec(content, glo, loc)  # pylint: disable=exec-used
    return loc["DEFINED_TEXTS"]


def load_ext_yml_data(ext_data):
    """Load external yaml data,
    raise exception if something is not ok."""
    import strictyaml  # pylint: disable=import-outside-toplevel

    content = ext_data.read_text(encoding="utf-8")
    return strictyaml.load(content).data


def load_sample_data():
    """Load provided sample data"""
    try:
        from .. import text_data  # pylint: disable=import-outside-toplevel
    except Exception:  # pylint: disable=broad-except
        # No data at all, return an empty dictionary
        return dict()
    return text_data.DEFINED_TEXTS
