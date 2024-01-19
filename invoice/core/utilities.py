import pathlib
import re
import traceback
from datetime import datetime
from types import NotImplementedType
from typing import Tuple

from . import file_io as io
from .profile import Profile


def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def delete_file(path):
    """delete file"""
    try:
        pathlib.Path(path).unlink()
    except Exception as e:
        print(f"Error deleting file: {e}")
        traceback.print_exc()


def concat_pos(column, row):
    """concat position"""
    return column + str(row)


def parse_keys(string, reg_pattern) -> list:
    r"""
    This function takes in a string and a regular expression pattern and returns a list of all matches found in the string.

    Parameters:
    - string (str): The input string to be parsed.
    - reg_pattern (str): The regular expression pattern to be used for matching.

    Returns:
    - matches (list): A list of all matches found in the string.

    Example:
    >>> parse_keys("Hello, World!", r"[A-Za-z]+")
    ['Hello', 'World']
    >>> parse_keys("Invoice {{provider.name}}-{{yymmdd}}", r"\{\{(.*?)\}\}")
    ['provider.name', 'yymmdd']
    """

    pattern = re.compile(reg_pattern)
    matches = pattern.findall(string)
    return matches


def categorize_key(string):
    # something.something
    if re.match(r"([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+)", string):
        return "json_path"
    if re.match(r"^[ymd]+$", string):
        return "date"
    else:
        raise NotImplementedType(f"Variable type not implemented: {string}")


def key_get_json_val(root, raw_key, is_list=False):
    keys = raw_key.split(".")
    if len(keys) < 1:
        raise ValueError(f"Invalid keys: {keys}")

    json_file = pathlib.Path(root, f"{keys[0]}.json")
    json_data = io.read_json(json_file)
    json_entry = json_data[int(keys[1])]
    for key in keys[2:]:
        if isinstance(json_entry, list):
            json_entry = json_entry[0]
        json_entry = json_entry[key]

    # Flatten the list if it contains only one element
    if isinstance(json_entry, list) and len(json_entry) == 1:
        return json_entry[0]
    return json_entry


def replace_keys(string: str, keys: list[str], seperator: Tuple[str, str]) -> str:
    result = string
    for key in keys:
        var_type = categorize_key(key)
        if var_type == "json_path":
            value = key_get_json_val("invoice/data/profiles", key)
            wrapped_key = f"{seperator[0]}{key}{seperator[1]}"
            if isinstance(value, list):
                raise ValueError(f"value is a list: {value}")
            result = result.replace(wrapped_key, value)
        if var_type == "date":
            value = convert_date(datetime.now(), key)
            wrapped_key = f"{seperator[0]}{key}{seperator[1]}"
            result = result.replace(wrapped_key, value)
    return result


def get_pdf_path(root, profile_name, invoice_number):
    """get pdf name"""
    # pdf file path
    profile_obj = Profile()
    profile = profile_obj.get_profile_by_name(profile_name)
    provider = profile_obj.get_provider_by_name(profile["provider"])
    privider_name_dict = io.search_json_by_key_value(provider["datas"], "label", "name")
    if privider_name_dict is not None:
        privider_name = privider_name_dict["value"]
    else:
        raise ValueError("Provider name not found")

    client = profile_obj.get_client_by_name(profile["client"])
    client_name_dict = io.search_json_by_key_value(client["datas"], "label", "name")
    if client_name_dict is not None:
        client_name = client_name_dict["value"]
    else:
        raise ValueError("Client name not found")

    # remove spaces
    privider_name = privider_name.replace(" ", "-")
    client_name = client_name.replace(" ", "-")

    pdf_name = f"{privider_name}_{client_name}_{invoice_number}.pdf"
    pdf_path = pathlib.Path(root, client_name, pdf_name)
    return pdf_path


def convert_date(date_obj: datetime, user_format: str):
    """
    Converts a given date object to a string representation based on the specified user format.

    Parameters:
    - date_obj (datetime.datetime): The date object to be converted.
    - user_format (str): The format string specified by the user. It can contain the following placeholders:
        - 'dd': Day of the month as a zero-padded decimal number (e.g., '01', '02', ..., '31').
        - 'mm': Month as a zero-padded decimal number (e.g., '01', '02', ..., '12').
        - 'yyyy': Year with century as a decimal number (e.g., '2021', '2022', ...).
        - 'yy': Year without century as a zero-padded decimal number (e.g., '21', '22', ...).
        - 'Mon': Abbreviated month name (e.g., 'Jan', 'Feb', ..., 'Dec').

    Returns:
    - str: The date object converted to a string representation based on the user format.

    Example:
    >>> from datetime import datetime
    >>> date_obj = datetime.now()
    >>> convert_date(date_obj, 'dd/mm/yyyy')
    '31/12/2021'
    >>> convert_date(date_obj, 'Mon dd, yyyy')
    'Dec 31, 2021'
    >>> convert_date(date_obj, 'yy-mm-dd')
    '21-12-31'
    >>> convert_date(date_obj, 'ddmmyy')
    '311221'
    """

    if not isinstance(date_obj, datetime):
        raise TypeError("date_obj must be a datetime.datetime object")

    if not isinstance(user_format, str):
        raise TypeError("user_format must be a string")

    format_mappings = {
        "dd": "%d",
        "mm": "%m",
        "yyyy": "%Y",
        "yy": "%y",
        "Mon": "%b",
    }

    datetime_format = user_format
    for key, value in format_mappings.items():
        datetime_format = datetime_format.replace(key, value)

    try:
        return date_obj.strftime(datetime_format)
    except ValueError:
        return "Invalid format"
