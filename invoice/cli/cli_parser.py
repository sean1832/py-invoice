import argparse

from invoice.cli import cli_commands as commands
from invoice.core.meta import metadata

def build_parser():
    """Build parser"""
    meta = metadata()
    parser = argparse.ArgumentParser(description=f'Invoice generator v{meta.version}')
    subparsers = parser.add_subparsers(help='commands')

    # version argument
    parser.add_argument('--version', action='store_true', help='Print version')

    # write command
    parser_create = subparsers.add_parser('write', 
                                          help='Create an invoice', 
                                          description='Create an invoice. If no arguments are provided, the invoice will be created with the default values.')
    parser_create.add_argument('profile_name', type=str, help='profile_name')
    parser_create.add_argument('date', type=str, help='Invoice date')
    parser_create.add_argument('--hour', type=float, help='Overwrite hours worked')
    parser_create.add_argument('--rate', type=float, help='Overwrite Hourly rate')
    parser_create.add_argument('--description', type=str, help='Overwrite description')
    parser_create.add_argument('--gst_code', type=float, help='Overwrite tax rate')
    
    parser_create.add_argument('--invoice_number', type=int, help='Overwrite invoice number')
    parser_create.add_argument('--template_path', type=str, help='Overwrite template path')
    parser_create.add_argument('--output', type=str, help='Overwrite output path')
    parser_create.add_argument('--append_row', action='store_true', help='Append row to existing invoice')
    parser_create.add_argument('--remove_last_row', action='store_true', help='Remove last row from existing invoice')
    parser_create.add_argument('--silent', action='store_true', help='Create invoice without preview')
    parser_create.set_defaults(func=commands.write)

    # delete command
    parser_delete = subparsers.add_parser('delete', help='Delete an invoice')
    parser_delete.add_argument('invoice_number', type=str, help='Invoice number, or "today" to delete today\'s invoice')
    parser_delete.set_defaults(func=commands.delete)

    # send command
    parser_send = subparsers.add_parser('send', help='Send an invoice')
    parser_send.add_argument('--profile_number', type=str, help='Profile number')
    parser_send.add_argument('--profile_name', type=str, help='Profile name')
    parser_send.add_argument('--email', type=str, help='Overwrite Target email address')
    parser_send.add_argument('--profile_path', type=str, help='Overwrite Path to profile file')
    parser_send.add_argument('--subject', type=str, help='Overwrite Subject of the email')
    parser_send.add_argument('--append_subject', type=str, help='Overwrite Msg to append to subject of the email')
    parser_send.add_argument('--body', type=str, help='Overwrite Body of the email')
    parser_send.add_argument('--append_body', type=str, help='Msg to append to body of the email')
    parser_send.add_argument('--attach', type=str, help='Overwrite Path of invoice attach to email')
    parser_send.add_argument('--silent', action='store_true', help='Send email without confirmation')
    parser_send.set_defaults(func=commands.send)

    # list command
    parser_list = subparsers.add_parser('list', help='List invoices')
    parser_list.set_defaults(func=commands.list)

    # show command
    parser_show = subparsers.add_parser('show', help='Show information')

    # Create one subparser for the show command
    show_subparsers = parser_show.add_subparsers(help='Show subcommands', dest='type')

    # show templates
    parser_show_template = show_subparsers.add_parser('template', help='Show templates')
    parser_show_template.set_defaults(func=commands.show_templates)

    # show profiles
    parser_show_profiles = show_subparsers.add_parser('profiles', help='Show profiles')
    parser_show_profiles.add_argument('profile_type', type=str, help='Profile type (client, provider)', choices=['client', 'provider'])
    parser_show_profiles.set_defaults(func=commands.show_profiles)

    # show invoice
    parser_show_invoice = show_subparsers.add_parser('invoice', help='Show invoice')
    parser_show_invoice.add_argument('invoice_number', type=str, help='Invoice number, or "today" to show today\'s invoice')
    parser_show_invoice.set_defaults(func=commands.show_invoice)

    # show config
    parser_show_config = show_subparsers.add_parser('config', help='Show config')
    parser_show_config.set_defaults(func=commands.show_config)

    

    return parser

