import json
import os

_appdata = os.getenv("APPDATA")
if _appdata is None:
    raise Exception("Environment variable APPDATA not found!")

APPDATA_ROOT = os.path.join(_appdata, "py-invoice")
APP_ROOT = os.path.dirname(os.path.dirname(__file__))
METADATA_PATH = os.path.join(APP_ROOT, "metadata.json")
CONFIG_PATH = os.path.join(APP_ROOT, "config.json")


class MetadataManager:
    def __init__(self):
        metadata = json.load(open(METADATA_PATH, "r"))
        self.name = metadata["name"]
        self.version = metadata["version"]
        self.description = metadata["description"]
        self.author = metadata["author"]
        self.url = metadata["url"]
        self.license = metadata["license"]


class PathManager:
    def __init__(self):
        self.config = CONFIG_PATH

        config_data = json.load(open(CONFIG_PATH, "r"))["path"]
        self.template = os.path.join(APP_ROOT, config_data["template"])
        self.credentials = os.path.join(APPDATA_ROOT, config_data["credentials"])
        self.key = os.path.join(APPDATA_ROOT, config_data["key"])
        self.instance = os.path.join(APPDATA_ROOT, config_data["instance"])
        self.output_dir = os.path.join(APPDATA_ROOT, config_data["output_dir"])

        profiles_path = config_data["profiles_path"]
        self.clients = os.path.join(APPDATA_ROOT, profiles_path["clients"])
        self.default_params = os.path.join(
            APPDATA_ROOT, profiles_path["default_params"]
        )
        self.profiles = os.path.join(APPDATA_ROOT, profiles_path["profiles"])
        self.providers = os.path.join(APPDATA_ROOT, profiles_path["providers"])
        self.recipients = os.path.join(APPDATA_ROOT, profiles_path["recipients"])

    def check_core_path(self, silent=False):
        attributes = ["config", "template"]

        file_not_found = []
        for attr in attributes:
            path = getattr(self, attr, None)
            if path and not os.path.exists(path):
                file_not_found.append(path)

        if len(file_not_found) > 0:
            if not silent:
                print(f"Files not found: {file_not_found}")
            return False

        return True

    def check_credential_path(self, silent=False):
        attributes = ["credentials", "key"]

        file_not_found = []
        for attr in attributes:
            path = getattr(self, attr, None)
            if path and not os.path.exists(path):
                file_not_found.append(path)

        if len(file_not_found) > 0:
            if not silent:
                print(f"Files not found: {file_not_found}")
            return False

        return True

    def check_profiles_path(self, silent=False):
        attributes = [
            "clients",
            "default_params",
            "profiles",
            "providers",
            "recipients",
        ]

        file_not_found = []
        for attr in attributes:
            path = getattr(self, attr, None)
            if path and not os.path.exists(path):
                file_not_found.append(path)

        if len(file_not_found) > 0:
            if not silent:
                print(f"Files not found: {file_not_found}")
            return False

        return True
