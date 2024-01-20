import json

from setuptools import find_packages, setup

meta = json.load(open("invoice/metadata.json", "r"))

setup(
    name=meta["name"],
    version=meta["version"],
    description=meta["description"],
    author=meta["author"],
    url=meta["url"],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": [
            "metadata.json",
            "config.json",
            "template.xlsx",
        ],
    },
    install_requires=[
        "openpyxl",
        "pywin32",
        "cryptography",
        "pandas",
    ],
    entry_points={"console_scripts": ["invoice = invoice.cli.cli_main:main"]},
)
