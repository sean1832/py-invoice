from invoice.core.file_io import read_json, search_json_by_key_value

from .config import path_info


class Profile:
    def __init__(self):
        self._path_info = path_info
        self.profile = None

    def get_profile_by_name(self, profile_name: str):
        """Get profile by name"""
        profile_file = read_json(self._path_info.profiles)
        profile = search_json_by_key_value(profile_file, "name", profile_name)
        if profile is None:
            raise ValueError(f"Profile not found: {profile_name}")
        self.profile = profile
        return profile

    def get_default_param_by_name(self, param_name: str):
        """Get default param by name"""
        default_params_file = read_json(self._path_info.default_params)
        param = search_json_by_key_value(default_params_file, "name", param_name)
        if param is None:
            raise ValueError(f"Default param not found: {param_name}")
        return param

    def get_client_by_name(self, client_name: str):
        """Get client by name"""
        clients_file = read_json(self._path_info.clients)
        client = search_json_by_key_value(clients_file, "name", client_name)
        if client is None:
            raise ValueError(f"Client not found: {client_name}")
        return client

    def get_provider_by_name(self, provider_name: str):
        """Get provider by name"""
        providers_file = read_json(self._path_info.providers)
        provider = search_json_by_key_value(providers_file, "name", provider_name)
        if provider is None:
            raise ValueError(f"Provider not found: {provider_name}")
        return provider

    def get_recipient_by_name(self, recipient_name: str):
        """Get recipient by name"""
        recipients_file = read_json(self._path_info.recipients)
        recipient = search_json_by_key_value(recipients_file, "name", recipient_name)
        if recipient is None:
            raise ValueError(f"Recipient not found: {recipient_name}")
        return recipient
