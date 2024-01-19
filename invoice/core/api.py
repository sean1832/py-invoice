from typing import Tuple

from invoice.core import utilities as utils
from invoice.core.excel_worker import Excel_worker
from invoice.core.profile import Profile

from . import file_io


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
    worker = Excel_worker(template_path, 0)

    if append:
        if not worker.is_instantiated():
            worker.instantiate()
            print("Appending file not found. Instantiated new file.")
        row = worker.get_last_data_row(date[0], iteration_start_row, row_range=5)
        if row is None:
            return
        else:
            row += 1
        print(f"Appending data to row {row}")
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
    profile_obj = Profile()
    profile = profile_obj.get_profile_by_name(profile_name)
    client = profile_obj.get_client_by_name(profile["client"])
    client_datas = client["datas"]
    for data in client_datas:
        if not data["location"] == "" or not data["value"] == "":
            worker.write_cell(data["location"], data["value"], data["type"])

    # write provider info
    provider = profile_obj.get_provider_by_name(profile["provider"])
    provider_datas = provider["datas"]
    for data in provider_datas:
        if not data["location"] == "" or not data["value"] == "":
            worker.write_cell(data["location"], data["value"], data["type"])


def remove_row(row_index: int, start_row: int, template_path: str):
    """remove a row from an invoice"""
    worker = Excel_worker(template_path, 0)
    worker.remove_row(row_index, start_row, row_range=5)

def clean_up():
    """Clean up"""
    # delete session cache
    file_io.delete_session_cache()

    # delete instance file
    Excel_worker().clean_up()

