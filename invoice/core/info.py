from invoice.core import file_io

metadata_path = 'invoice/metadata.json'
config_path = 'invoice/data/config.json'

class Meta_info:
    def __init__(self):
        self.name = file_io.read_json(metadata_path)['name']
        self.version = file_io.read_json(metadata_path)['version']
        self.description = file_io.read_json(metadata_path)['description']
        self.author = file_io.read_json(metadata_path)['author']
        self.url = file_io.read_json(metadata_path)['url']
        self.license = file_io.read_json(metadata_path)['license']

class Path_info:
    def __init__(self):
        self.config = config_path
        self.template = file_io.read_json(config_path)['path']['template']
        self.credentials = file_io.read_json(config_path)['path']['credentials']
        self.key = file_io.read_json(config_path)['path']['key']
        self.instance = file_io.read_json(config_path)['path']['instance']
        self.output_dir = file_io.read_json(config_path)['path']['output_dir']
        self.clients = file_io.read_json(config_path)['path']['profiles_path']['clients']
        self.default_params = file_io.read_json(config_path)['path']['profiles_path']['default_params']
        self.profiles = file_io.read_json(config_path)['path']['profiles_path']['profiles']
        self.providers = file_io.read_json(config_path)['path']['profiles_path']['providers']
        self.recipients = file_io.read_json(config_path)['path']['profiles_path']['recipients']
        