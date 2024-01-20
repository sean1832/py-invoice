import os
import pathlib
from datetime import datetime

from .profile import Client, Profile, Provider


def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def concat_pos(column, row):
    """concat position"""
    return column + str(row)


def print_dataframe_in_grid(df, max_width=100):
    """Prints the DataFrame in a grid format in the terminal."""
    if df is None:
        return
    # Get terminal width and adjust with scaling factor
    terminal_width = os.get_terminal_size().columns
    adjusted_width = int(terminal_width * (max_width / 100))

    # Calculate total width used for separators
    total_separator_width = 3 * len(df.columns) + 1

    # Calculate available width for data
    available_width = adjusted_width - total_separator_width

    # Find the maximum width of each column and sum
    col_max_widths = [df[col].astype(str).map(len).max() for col in df.columns]
    total_width = sum(col_max_widths)

    # Scale column widths based on available width
    col_widths = [
        int((width / total_width) * available_width) for width in col_max_widths
    ]

    # Print the horizontal line
    def print_horizontal_line():
        line = "+"
        for width in col_widths:
            line += "-" * (width + 2) + "+"
        print(line)

    print_horizontal_line()

    # Print each row with vertical separators
    for _, row in df.iterrows():
        row_str = (
            "| "
            + " | ".join(
                f"{str(row[col])[:col_widths[i]].ljust(col_widths[i])}"
                for i, col in enumerate(df.columns)
            )
            + " |"
        )
        print(row_str)
        print_horizontal_line()


def get_pdf_path(root, profile_name, invoice_number):
    """get pdf name"""
    # pdf file path
    profile = Profile(profile_name)
    provider = Provider(profile)
    provider_dataitem = provider.querry_data_label("name")
    if provider_dataitem is not None:
        privider_name = provider_dataitem.value
    else:
        raise ValueError("Provider name not found")

    client = Client(profile)
    client_dataitem = client.querry_data_label("name")
    if client_dataitem is not None:
        client_name = client_dataitem.value
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
