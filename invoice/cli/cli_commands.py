import pathlib
from datetime import datetime
from pathlib import Path

from invoice.core import api, credentials, file_io, smtp, utilities
from invoice.core.config import path_info
from invoice.core.profile import DefaultParam, Profile, Recipient

from . import cli_prompt


def write(args):
    """Create invoice"""
    if not path_info.check_profiles_path():
        print(
            "Profiles path not found. Please run 'invoice init' to create profiles. \nNote: that you may have to manually edit the contents."
        )
        return
    profile_name = args.profile_name

    # parse default_param.json file to get default values
    profile = Profile(profile_name)
    param = DefaultParam(profile)

    # date
    date_val = args.date
    date_loc = param.iteration.date.column
    date = (date_loc, date_val)

    # iteration_start_row
    iteration_start_row = param.iteration.start_row
    # hour
    hour_loc = param.iteration.unit.column
    hour_val = args.hour
    if hour_val is None:
        if param.iteration.unit.value is None:
            raise ValueError("Hour value not found")
        hour = (hour_loc, float(param.iteration.unit.value))
    else:
        hour = (hour_loc, float(hour_val))

    # rate
    rate_loc = param.iteration.rate.column
    rate_val = args.rate
    if rate_val is None:
        if param.iteration.rate.value is None:
            raise ValueError("Rate value not found")
        rate = (rate_loc, float(param.iteration.rate.value))
    else:
        rate = (rate_loc, float(rate_val))

    # description
    description_loc = param.iteration.description.column
    description_val = args.description
    if description_val is None:
        if param.iteration.description.value is None:
            raise ValueError("Description value not found")
        description = (description_loc, param.iteration.description.value)
    else:
        description = (description_loc, description_val)

    # gst_code
    gst_code_loc = param.iteration.gst_code.column
    gst_code_val = args.gst_code
    if gst_code_val is None:
        if param.iteration.gst_code.value is None:
            raise ValueError("GST code value not found")
        gst_code = (gst_code_loc, param.iteration.gst_code.value)
    else:
        gst_code = (gst_code_loc, gst_code_val)

    # invoice_number
    invoice_number_loc = param.invoice_number.location
    invoice_number_val = args.invoice_number
    if invoice_number_val is None:
        invoice_num_format = param.invoice_number.value
        invoice_number = (
            invoice_number_loc,
            utilities.convert_date(datetime.now(), invoice_num_format),
        )
    else:
        invoice_number = (invoice_number_loc, invoice_number_val)

    # invoice_date
    invoice_date_loc = param.invoice_date.location
    invoice_date_val = utilities.convert_date(datetime.now(), "dd/mm/yyyy")
    invoice_date = (invoice_date_loc, invoice_date_val)

    # template_path
    template_path = args.template_path
    if template_path is None:
        template_path = path_info.template
    else:
        if not Path(template_path).exists() or not Path(template_path).is_file():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        if not template_path.endswith(".xlsx"):
            raise ValueError("Template file must be an Excel file")

    # calculate amount
    amount_val = hour[1] * rate[1]
    amount_loc = param.iteration.amount.column
    amount = (amount_loc, amount_val)

    # flags
    append_row = args.append
    silent = args.silent

    df = api.write_datas(
        profile_name,
        iteration_start_row,
        date,
        hour,
        rate,
        description,
        amount,
        gst_code,
        invoice_number,
        invoice_date,
        template_path,
        append_row,
        silent,
    )
    utilities.print_dataframe_in_grid(df, 70)

    # write to cache
    cache_data = {
        "profile_name": profile_name,
        "date": date[1],
        "hour": hour[1],
        "rate": rate[1],
        "description": description[1],
        "gst_code": gst_code[1],
        "invoice_number": invoice_number[1],
        "template_path": template_path,
        "append": append_row,
        "silent": silent,
        "timestamp": datetime.now().timestamp(),
    }
    file_io.create_session_cache(cache_data)


def remove(args):
    """remove a row from an invoice"""
    if not path_info.check_profiles_path():
        print(
            "Profiles path not found. Please run 'invoice init' to create profiles. \nNote: that you may have to manually edit the contents."
        )
        return
    # read session cache
    cache_data = file_io.read_session_cache()

    profile = Profile(cache_data["profile_name"])
    param = DefaultParam(profile)
    template_path = path_info.template
    start_row = param.iteration.start_row
    df = api.remove_row(args.row_index, start_row, template_path)
    utilities.print_dataframe_in_grid(df, 70)


def export(args):
    """export an invoice to pdf"""
    if not path_info.check_profiles_path():
        print(
            "Profiles path not found. Please run 'invoice init' to create profiles. \nNote: that you may have to manually edit the contents."
        )
        return
    # read session cache
    cache_data = file_io.read_session_cache()
    profile_name = cache_data["profile_name"]
    invoice_number = cache_data["invoice_number"]

    # excel file path
    instance_path = path_info.instance

    # output dir for pdf
    pdf_output_dir = path_info.output_dir

    # pdf file path
    pdf_path = utilities.get_pdf_path(pdf_output_dir, profile_name, invoice_number)

    file_io.excel_to_pdf(instance_path, pdf_path)

    cache_data["pdf_path"] = str(pdf_path)
    file_io.create_session_cache(cache_data)


def send(args):
    """Send an invoice"""
    if not path_info.check_profiles_path():
        print(
            "Profiles path not found. Please run 'invoice init' to create profiles. \nNote: that you may have to manually edit the contents."
        )
        return
    if not path_info.check_credential_path():
        print(
            "Credentials path not found. Please run 'invoice login' to set up credentials"
        )
        return

    cache_data = file_io.read_session_cache()
    profile_name = cache_data["profile_name"]
    profile = Profile(profile_name)
    recipient = Recipient(profile)

    print("=== Email ===")

    # email
    print(recipient.email)

    # subject
    subject_raw = recipient.subject
    # parse subject
    subject_keys = utilities.parse_keys(subject_raw, r"\{\{(.*?)\}\}")
    subject = utilities.replace_keys(subject_raw, subject_keys, (r"{{", r"}}"))
    print(subject)

    # body
    body = recipient.body
    # parse body
    body_keys = utilities.parse_keys(body, r"\{\{(.*?)\}\}")
    body = utilities.replace_keys(body, body_keys, (r"{{", r"}}"))
    print(body)

    # read config
    config = file_io.read_json(path_info.config)["smtp"]
    smtp_host = config["host"]
    smtp_port = config["port"]

    email, password = credentials.decrypt_from_json()

    server = smtp.Smtp(smtp_host, smtp_port, email, password)
    print("=== Attachment ===")
    print(cache_data["pdf_path"])

    print("=== Confirmation ===")
    user_input = input("Send email? (y/n)")
    if user_input.lower() != "y":
        print("Aborted.")
        return

    # validate email
    if not args.skip:
        print("=== Login ===")
        is_valid, error = server.validate()
        if not is_valid:
            print(
                f"Login failed. Please run 'invoice login' to set up credentials.\n{error}"
            )
            return
        else:
            print("Login successful!")

    print("=== Sending email ===")
    server.send_email(recipient.email, subject, body, cache_data["pdf_path"])
    print("Email sent successfully!")

    print("=== Clean up ===")
    # clean up
    api.clean_up()
    print("Clean up successful!")


def login(args):
    """Set up credentials"""
    config = file_io.read_json(path_info.config)["smtp"]
    smtp_host = config["host"]
    smtp_port = config["port"]

    while True:
        email, password = cli_prompt.login_prompt(args.show)
        result, error = api.login(smtp_host, smtp_port, email, password)
        if result:
            print("Login successful!")
            break
        else:
            print(f"Login failed. {error}")


def init(args):
    """Create dummy data"""
    if path_info.check_profiles_path():
        asw = input("Profiles path already exists. Do you want to overwrite it? (y/n)")
        if asw == "n":
            print("Aborted.")
            return

    api.dummy.create_dummy()
    print("Dummy data created successfully!")

    # login

    config = file_io.read_json(path_info.config)["smtp"]
    profile_root = pathlib.Path(path_info.profiles).parent
    smtp_host = config["host"]
    smtp_port = config["port"]

    while True:
        email, password = cli_prompt.login_prompt(args.show)
        result, error = api.login(smtp_host, smtp_port, email, password)
        if result:
            print("Login successful!")
            break
        else:
            print(f"Login failed. {error}")

    file_io.open_directory(profile_root)


def list(args):
    """List invoices"""
    raise NotImplementedError


def show_profiles(args):
    """Show profiles"""
    profile_root = pathlib.Path(path_info.profiles).parent
    file_io.open_directory(profile_root)


def show_invoice(args):
    """Show invoice"""


def show_config(args):
    """Show config"""
    raise NotImplementedError
