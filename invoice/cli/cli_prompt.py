import getpass


def login_prompt(show_password=False):
    """Prompt for password"""
    email = input("Enter email: ")
    if show_password:
        password = input("Enter password: ")
    else:
        password = getpass.getpass("Enter password: ")
    return email, password
