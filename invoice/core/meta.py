from invoice.core import file_io

path = 'invoice/metadata.json'

class metadata:
    def __init__(self):
        self.name = file_io.read_json(path)['name']
        self.version = file_io.read_json(path)['version']
        self.description = file_io.read_json(path)['description']
        self.author = file_io.read_json(path)['author']
        self.url = file_io.read_json(path)['url']
        self.license = file_io.read_json(path)['license']