from typing import Tuple

from invoice.core import utilities as utils
from invoice.core.excel_worker import ExcelWorker
from invoice.core.profile import Client, Profile, Provider

from . import credentials, dummy, smtp  # noqa: F401


def write_datas(
    profile_name: str,
    iteration_start_row: int,
    date: Tuple[str, str],
    hour: Tuple[str, float],
    rate: Tuple[str, float],
    description: Tuple[str, str],
    amount: Tuple[str, float],
    gst_code: Tuple[str, str],
    invoice_number: Tuple[str, str],
    invoice_date: Tuple[str, str],
    template_path: str,
    append: bool,
    silent: bool,
):
    """Create invoice"""
    worker = ExcelWorker(template_path, 0)

    if append:
        if not worker.is_instantiated():
            worker.instantiate()
            print("Appending file not found. Instantiated new file.")
        row = worker.get_last_data_row(date[0], iteration_start_row, row_range=5)
        if row is None:
            return
        else:
            row += 1
    else:
        row = iteration_start_row
        worker.instantiate()

    # write date
    date_loc = utils.concat_pos(date[0], row)
    worker.write_cell(date_loc, date[1])

    # write hour
    hour_loc = utils.concat_pos(hour[0], row)
    worker.write_cell(hour_loc, hour[1], "float")

    # write rate
    rate_loc = utils.concat_pos(rate[0], row)
    worker.write_cell(rate_loc, rate[1], "currency")

    # write description
    description_loc = utils.concat_pos(description[0], row)
    worker.write_cell(description_loc, description[1])

    # write amount
    amount_loc = utils.concat_pos(amount[0], row)
    worker.write_cell(amount_loc, amount[1], "currency")

    # write gst code
    gst_code_loc = utils.concat_pos(gst_code[0], row)
    worker.write_cell(gst_code_loc, gst_code[1])

    # write invoice number
    worker.write_cell(invoice_number[0], invoice_number[1], "string")

    # write invoice date
    worker.write_cell(invoice_date[0], invoice_date[1])

    # write client info
    profile = Profile(profile_name)
    client = Client(profile)
    for data in client.datas:
        if not data.location == "" or not data.value == "":
            worker.write_cell(data.location, data.value, data.type)

    # write provider info
    provider = Provider(profile)
    for data in provider.datas:
        if not data.location == "" or not data.value == "":
            worker.write_cell(data.location, data.value, data.type)
    return worker.read_range("a17", "f22")

def login(smtp_host, smtp_port, email, password):
    server = smtp.Smtp(
        smtp_host, smtp_port, email, password
    )
    is_login, error = server.validate()
    if is_login:
        credentials.encrypt_to_json(email, password, hidden=False)
        return True, ""
    else:
        return False, error
        

def remove_row(row_index: int, start_row: int, template_path: str):
    """remove a row from an invoice"""
    worker = ExcelWorker(template_path, 0)
    try:
        worker.remove_row(row_index, start_row, row_range=5)
    except Exception:
        return None
    return worker.read_range("a17", "f22")

def clean_up():
    """Clean up"""
    # # delete session cache
    # file_io.delete_session_cache()

    # delete instance file
    ExcelWorker().clean_up()

