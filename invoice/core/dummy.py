from . import file_io, info


def create_clients():
    data = [
        {
            "id": 0,
            "name": "Client 1",
            "datas":[
                {
                    "label": "name",
                    "value": "Client 1",
                    "location": "b10",
                    "type": "string"
                },
                {
                    "label": "address",
                    "value": "somewhere",
                    "location": "b11",
                    "type": "string"
                },
                {
                    "label": "abn",
                    "value": "",
                    "location": "",
                    "type": "string"
                },
                {
                    "label": "email",
                    "value": "",
                    "location": "",
                    "type": "string"
                },
                {
                    "label": "phone",
                    "value": "12345678",
                    "location": "b12",
                    "type": "string"
                },
                {
                    "label": "url",
                    "value": "",
                    "location": "",
                    "type": "string"
                }
            ]
        }
    ]
    path = info.PathInfo().clients
    file_io.write_json(path, data)

def create_default_params():
    data = [
        {
            "id": 0,
            "name": "default",
            "description": "default parameters for invoice",
            "invoice_date": {
                "value": "dd/mm/yyyy",
                "location": "f15"
            },
            "invoice_number": {
                "value": "yymmdd",
                "location": "e15"
            },
            "iteration":{
                "start_row": 18,
                "date":{
                    "column": "a"
                },
                "unit":{
                    "column": "b",
                    "value": 6
                },
                "rate":{
                    "column": "c",
                    "value": 40
                },
                
                "description":{
                    "column": "d",
                    "value": "Service Charge"
                },
                "amount" : {
                    "column": "e"
                },
                "gst_code":{
                    "column": "f",
                    "value": "Free"
                }
            }
        }
    ]
    path = info.PathInfo().default_params
    file_io.write_json(path, data)

def create_profiles():
    data = [
        {
            "id": 0,
            "name": "default",
            "params": "default",
            "provider": "Provider 1",
            "client": "Client 1",
            "recipient": "pm"
        }
    ]
    path = info.PathInfo().profiles
    file_io.write_json(path, data)

def create_providers():
    data = [
        {
            "id": 0,
            "name": "Provider 1",
            "datas": [
                {
                    "label": "name",
                    "value": "Provider 1",
                    "location": "b3",
                    "type": "string"
                },
                {
                    "label": "address",
                    "value": "xxxxxxxx",
                    "location": "b4",
                    "type": "string"
                },
                {
                    "label": "abn",
                    "value": "123456789",
                    "location": "b5",
                    "type": "string"
                },
                {
                    "label": "email",
                    "value": "something@email.com",
                    "location": "b6",
                    "type": "string"
                },
                {
                    "label": "phone",
                    "value": "123456789",
                    "location": "b7",
                    "type": "string"
                },
                {
                    "label": "url",
                    "value": "",
                    "location": "",
                    "type": "string"
                },
                {
                    "label": "payment_method",
                    "value": "EFT Payment",
                    "location": "a31",
                    "type": "string"
                },
                {
                    "label": "account_name",
                    "value": "Provider 1",
                    "location": "b31",
                    "type": "string"
                },
                {
                    "label": "bsb",
                    "value": "123456",
                    "location": "c31",
                    "type": "string"
                },
                {
                    "label": "account_number",
                    "value": "12345678",
                    "location": "d31",
                    "type": "string"
                }
            ]
        }
    ]
    path = info.PathInfo().providers
    file_io.write_json(path, data)

def create_recipients():
    data = [
        {
            "id": 0,
            "name": "pm",
            "description": "account",
            "email": "something@email.com",
            "subject": "Invoice from {{providers.0.name}} - {{yymmdd}}",
            "body": "Please find attached the invoice for the services rendered. \n\nRegards\n{{providers.0.name}}"
        }
    ]
    path = info.PathInfo().recipients
    file_io.write_json(path, data)

def create_dummy():
    create_clients()
    create_default_params()
    create_profiles()
    create_providers()
    create_recipients()