"""
ClipTools clipboard manager and text processing tools
with a lines based GUI interface

Configurations, default values and reading user configs.
"""

import pathlib
from dataclasses import dataclass

import strictyaml


@dataclass
class Config:
    """
    Configurations for ClipTools
    """

    # configurable values
    port: int = 5555
    number_of_rows: int = 9
    max_number_of_data: int = 50
    string_length: int = 30
    use_py_per_clip: bool = True
    # constants
    server_success: str = "CLIP-OK."


schema = strictyaml.Map(
    {
        "Configurations": strictyaml.Map(
            {
                strictyaml.Optional("port"): strictyaml.Int(),
                strictyaml.Optional("number_of_rows"): strictyaml.Int(),
                strictyaml.Optional("max_number_of_data"): strictyaml.Int(),
                strictyaml.Optional("string_length"): strictyaml.Int(),
                strictyaml.Optional("use_py_per_clip"): strictyaml.Bool(),
            }
        )
    }
)


def read_config(
    user_folder: pathlib.Path, *, config_file: pathlib.Path | None = None
) -> Config | str:
    """
    Read the user configurations from config.yml in the user folder.

    config_file can be given directly, but that is only for testing.
    """
    config = Config()
    if config_file is None:
        config_file = user_folder / "config.yml"
    if not config_file.is_file():
        return f"Config file {config_file} not found"
    try:
        config_text = config_file.read_text(encoding="utf-8")
    except OSError:
        return f"Cannot read donfig file {config_file}"
    try:
        raw_config = strictyaml.load(config_text, schema).data
    except strictyaml.StrictYAMLError as exc:
        return f"Config YAML error: {exc}"
    for k, v in raw_config["Configurations"].items():
        setattr(config, k, v)
    return config
