from invoice.core.file_io import read_json, search_json_by_key_value

from .config import path_info


class Profile:
    def __init__(self, profile_name: str):
        profile = self._get_profile_by_name(profile_name)
        self.id = profile["id"]
        self.name = profile_name
        self.params = profile["params"]
        self.client = profile["client"]
        self.provider = profile["provider"]
        self.recipient = profile["recipient"]

    def _get_profile_by_name(self, profile_name: str):
        """Get profile by name"""
        profile_file = read_json(path_info.profiles)
        profile = search_json_by_key_value(profile_file, "name", profile_name)
        if profile is None:
            raise ValueError(f"Profile not found: {profile_name}")
        self.profile = profile
        return profile


class _DataItem:
    def __init__(self, label, value, location, type="string"):
        self.label = label
        self.value = value
        self.location = location
        self.type = type


class Client:
    def __init__(self, profile: Profile):
        client = self._get_client_by_name(profile.client)
        self.id = client["id"]
        self.name = client["name"]
        self.datas: list[_DataItem] = self._get_datas(client["datas"])

    def _get_client_by_name(self, client_name: str):
        """Get client by name"""
        clients_file = read_json(path_info.clients)
        client = search_json_by_key_value(clients_file, "name", client_name)
        if client is None:
            raise ValueError(f"Client not found: {client_name}")
        return client

    def _get_datas(self, datas: list[dict]):
        result = []
        for data in datas:
            result.append(_DataItem(**data))
        return result

    def querry_data_label(self, label: str):
        """Get data by label"""
        for data in self.datas:
            if data.label == label:
                return data
        return None


class Provider:
    def __init__(self, profile: Profile):
        provider = self._get_provider_by_name(profile.provider)
        self.id = provider["id"]
        self.name = provider["name"]
        self.datas: list[_DataItem] = self._get_datas(provider["datas"])

    def _get_provider_by_name(self, provider_name: str):
        """Get provider by name"""
        providers_file = read_json(path_info.providers)
        provider = search_json_by_key_value(providers_file, "name", provider_name)
        if provider is None:
            raise ValueError(f"Provider not found: {provider_name}")
        return provider

    def _get_datas(self, datas: list[dict]):
        result = []
        for data in datas:
            result.append(_DataItem(**data))
        return result

    def querry_data_label(self, label: str):
        """Get data by label"""
        for data in self.datas:
            if data.label == label:
                return data
        return None


class _IterationComponent:
    def __init__(self, column: str, value: str | None):
        self.column = column
        self.value = value


class _Iteration:
    def __init__(self, date, amount, unit, rate, description, gst_code, start_row: int):
        self.date = _IterationComponent(**date)
        self.amount = _IterationComponent(**amount)
        self.unit = _IterationComponent(**unit)
        self.rate = _IterationComponent(**rate)
        self.description = _IterationComponent(**description)
        self.gst_code = _IterationComponent(**gst_code)
        self.start_row = start_row


class DefaultParam:
    def __init__(self, profile: Profile):
        param = self._get_default_param_by_name(profile.params)
        self.id = param["id"]
        self.name = param["name"]
        self.description = param["description"]
        self.invoice_date = _DataItem(**param["invoice_date"])
        self.invoice_number = _DataItem(**param["invoice_number"])
        self.iteration = _Iteration(**param["iteration"])

    def _get_default_param_by_name(self, param_name: str):
        """Get default param by name"""
        default_params_file = read_json(path_info.default_params)
        param = search_json_by_key_value(default_params_file, "name", param_name)
        if param is None:
            raise ValueError(f"Default param not found: {param_name}")
        return param


class Recipient:
    def __init__(self, profile: Profile):
        recipient = self._get_recipient_by_name(profile.recipient)
        self.id = recipient["id"]
        self.name = recipient["name"]
        self.description = recipient["description"]
        self.email = recipient["email"]
        self.subject = recipient["subject"]
        self.body = recipient["body"]

    def _get_recipient_by_name(self, recipient_name: str):
        """Get recipient by name"""
        recipients_file = read_json(path_info.recipients)
        recipient = search_json_by_key_value(recipients_file, "name", recipient_name)
        if recipient is None:
            raise ValueError(f"Recipient not found: {recipient_name}")
        return recipient
