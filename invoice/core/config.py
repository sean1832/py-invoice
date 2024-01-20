from . import config_manager

METADATA_PATH = 'invoice/metadata.json'
CONFIG_PATH = 'invoice/data/config.json'

path_info = config_manager.PathManager()
project_meta = config_manager.MetadataManager()