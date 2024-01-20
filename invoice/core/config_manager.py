import os

from invoice.core import file_io

METADATA_PATH = 'invoice/metadata.json'
CONFIG_PATH = 'invoice/data/config.json'

class MetadataManager:
    def __init__(self):
        metadata = file_io.read_json(METADATA_PATH)
        self.name = metadata['name']
        self.version = metadata['version']
        self.description = metadata['description']
        self.author = metadata['author']
        self.url = metadata['url']
        self.license = metadata['license']

class PathManager:
    def __init__(self):
        self.config = CONFIG_PATH

        config_data = file_io.read_json(CONFIG_PATH)['path']
        self.template = config_data['template']
        self.credentials = config_data['credentials']
        self.key = config_data['key']
        self.instance = config_data['instance']
        self.output_dir = config_data['output_dir']

        profiles_path = config_data['profiles_path']
        self.clients = profiles_path['clients']
        self.default_params = profiles_path['default_params']
        self.profiles = profiles_path['profiles']
        self.providers = profiles_path['providers']
        self.recipients = profiles_path['recipients']
        
    def check_core_path(self):
        attributes = ['config', 'template']

        file_not_found = []
        for attr in attributes:
            path = getattr(self, attr, None)
            if path and not os.path.exists(path):
                file_not_found.append(path)
        
        if len(file_not_found) > 0:
            print(f"Files not found: {file_not_found}")
            return False

        return True
    
    def check_credential_path(self):
        attributes = ['credentials', 'key']

        file_not_found = []
        for attr in attributes:
            path = getattr(self, attr, None)
            if path and not os.path.exists(path):
                file_not_found.append(path)
        
        if len(file_not_found) > 0:
            print(f"Files not found: {file_not_found}")
            return False

        return True

    def check_profiles_path(self):
        attributes = ['clients', 'default_params', 'profiles', 'providers', 'recipients']

        file_not_found = []
        for attr in attributes:
            path = getattr(self, attr, None)
            if path and not os.path.exists(path):
                file_not_found.append(path)

        if len(file_not_found) > 0:
            print(f"Files not found: {file_not_found}")
            return False

        return True