import json
import os
import pathlib
import shutil
import subprocess
import sys
import traceback

import win32api
import win32com.client


def read_json(path):
    return json.load(open(path, "r"))

def write_json(path: str | pathlib.Path, content):
    # create directory if not exists
    path = pathlib.Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    json.dump(content, open(path, "w"), indent=4)
def search_json_by_key_value(json, key, value):
    for item in json:
        if item[key] == value:
            return item
    return None

def delete_file(path):
    """delete file"""
    try:
        pathlib.Path(path).unlink()
    except Exception as e:
        print(f"Error deleting file: {e}")
        traceback.print_exc()

def search_json_list_by_key_value(json, key, value):
    result = []
    for item in json:
        print(value)
        if isinstance(item, dict) and item[key] == value:
            if item[key] == value:
                result.append(item)
    return result

def open_directory(path):
    # Check if the path is a valid directory
    if not os.path.isdir(path):
        print(f"The path {path} is not a valid directory.")
        return

    # check if vscode is installed
    if shutil.which("code"):
        full_path = pathlib.Path(path).resolve()
        print(f"Opening directory in vscode {full_path}")
        subprocess.run(["code", full_path], shell=True)
        return
    # Open the directory based on the operating system
    if sys.platform == 'win32':
        subprocess.run(['explorer', path])
    elif sys.platform == 'darwin':  # macOS
        subprocess.run(['open', path])
    else:  # Linux and other Unix-like OS
        subprocess.run(['xdg-open', path])

def open_file(path):
    # Check if the path is a valid file
    if not os.path.isfile(path):
        print(f"The path {path} is not a valid file.")
        return
    
    # Open the file based on the operating system
    if sys.platform == 'win32':
        subprocess.run(['start', path], shell=True)
    elif sys.platform == 'darwin':  # macOS
        subprocess.run(['open', path])
    else:  # Linux and other Unix-like OS
        subprocess.run(['xdg-open', path])


def read_bytes(path: pathlib.Path | str):
    with open(path, "rb") as f:
        content = f.read()
    return content

def write_bytes(path: pathlib.Path | str, content: bytes):
    with open(path, "wb") as f:
        f.write(content)

def create_session_cache(content: dict):
    """Create session cache"""
    cache_path = pathlib.Path("invoice/data/session_cache.temp")
    # write as json
    with open(cache_path, "w") as f:
        json.dump(content, f)


def read_session_cache():
    """Read session cache"""
    cache_path = pathlib.Path("invoice/data/session_cache.temp")
    # read as json
    with open(cache_path, "r") as f:
        content = json.load(f)
    return content


def delete_session_cache():
    """Delete session cache"""
    cache_path = pathlib.Path("invoice/data/session_cache.temp")
    cache_path.unlink()


def make_file_hidden(path):
    """Create hidden file"""
    path = pathlib.Path(path)
    if path.exists() is False:
        raise FileNotFoundError(f"File not found: {path}")

    FILE_ATTRIBUTE_HIDDEN = 0x02
    win32api.SetFileAttributes(str(path.resolve()), FILE_ATTRIBUTE_HIDDEN)


def excel_to_pdf(excel_path, pdf_path):
    """Convert excel to pdf"""

    # validate input
    if pathlib.Path(excel_path).suffix != ".xlsx":
        raise ValueError("Invalid excel file!")
    if pathlib.Path(pdf_path).suffix != ".pdf":
        raise ValueError("Invalid pdf file!")

    # convert to absolute path
    excel_path = pathlib.Path(excel_path).resolve()
    pdf_path = pathlib.Path(pdf_path).resolve()

    # create directory if not exists
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    excel = None
    wb = None
    try:
        excel_path = pathlib.Path(excel_path)
        pdf_path = pathlib.Path(pdf_path)
        if excel_path.is_file() is False:
            raise FileNotFoundError("Excel file not found!")

        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False

        wb = excel.Workbooks.Open(excel_path)
        wb.ActiveSheet.ExportAsFixedFormat(0, str(pdf_path))
        return pdf_path
    except Exception as e:
        print(f"Error converting excel to pdf: {e}")
        traceback.print_exc()
        return None
    finally:
        if wb is not None:
            wb.Close()
        if excel is not None:
            excel.Quit()
