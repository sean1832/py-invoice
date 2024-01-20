import pathlib
from typing import Any

from cryptography.fernet import Fernet

from . import file_io
from .config import path_info


def encrypt_value(value: Any, key: bytes) -> str:
    """Encrypt value"""
    f = Fernet(key)
    return f.encrypt(value.encode()).decode()

def decrypt_value(value: str, key: bytes) -> str:
    """Decrypt value"""
    f = Fernet(key)
    return f.decrypt(value.encode()).decode()

def read_key() -> bytes:
    """Read key"""
    if not pathlib.Path(path_info.key).exists():
        raise FileNotFoundError("Key file not found")
    return file_io.read_bytes(path_info.key)

def read_credentials() -> dict[str, str]:
    """Read credentials"""
    if not pathlib.Path(path_info.credentials).exists():
        raise FileNotFoundError("Credentials file not found")
    return file_io.read_json(path_info.credentials)

def encrypt_to_json(email: str, password: str, hidden: bool = False):
    """Encrypt email and password to json"""
    
    # generate key
    key = Fernet.generate_key()
    encrypted_email = encrypt_value(email, key)
    encrypted_password = encrypt_value(password, key)
    credentials = {
        "email": encrypted_email,
        "password": encrypted_password,
    }
    # write to encrypted value and key to file
    file_io.write_json(path_info.credentials, credentials)
    file_io.write_bytes(path_info.key, key)

    if hidden:
        # make credentials and key hidden
        file_io.make_file_hidden(path_info.credentials)
        file_io.make_file_hidden(path_info.key)


def decrypt_from_json() -> tuple[str, str]:
    """
    Decrypt email and password from json.

    Returns:
        tuple[str, str]: (email, password)
    """
    credentials = read_credentials()
    key = read_key()
    email = decrypt_value(credentials["email"], key)
    password = decrypt_value(credentials["password"], key)
    return email, password