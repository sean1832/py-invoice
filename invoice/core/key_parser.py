import re
from datetime import datetime
from typing import Tuple

from . import utilities
from .profile import Client, DefaultParam, Profile, Provider, Recipient


class KeyParser:
    r"""
    Example:
    >>> parser = KeyParser("{{provider.name}}-{{yymmdd}}", r"\{\{(.*?)\}\}")
    """

    def __init__(self, string: str, reg_pattern: str, profile_name: str):
        self.string = string
        self.reg_pattern = reg_pattern
        self.profile_name = profile_name

    def parse(self) -> list:
        """Example:
        >>> parse_keys()
        ['provider.name', 'yymmdd']"""

        pattern = re.compile(self.reg_pattern)
        matches = pattern.findall(self.string)
        return matches

    def replace_keys(self, keys: list[str], seperator: Tuple[str, str]) -> str:
        result = self.string
        for key in keys:
            var_type = self._categorize_key(key)
            if var_type == "code":
                value = self._process_code_str(key)
            elif var_type == "date":
                value = utilities.convert_date(datetime.now(), key)
            else:
                raise NotImplementedError(f"Variable type not implemented: {key}")
            wrapped_key = f"{seperator[0]}{key}{seperator[1]}"
            result = result.replace(wrapped_key, value)
        return result

    @staticmethod
    def _categorize_key(key):
        # something.something
        if re.match(
            r"([a-zA-Z0-9_\[\]\(\)\"\'\ ]+(?:\.[a-zA-Z0-9_\[\]\(\)\"\'\ ]+)+)",
            key,
        ):
            return "code"
        if re.match(r"^[ymd]+$", key):
            return "date"
        else:
            raise NotImplementedError(f"Variable type not implemented: {key}")

    def _process_code_str(self, code: str):
        """Process code"""
        # import variables
        profile = Profile(self.profile_name)
        provider = Provider(profile)  # noqa: F841
        client = Client(profile)  # noqa: F841
        recipient = Recipient(profile)  # noqa: F841
        default_param = DefaultParam(profile)  # noqa: F841

        # evaluate code to get value
        return eval(code)
