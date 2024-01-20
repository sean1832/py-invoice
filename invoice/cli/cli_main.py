from invoice.cli import cli_parser
from invoice.core import config_manager


def main():
    parser = cli_parser.build_parser()
    args = parser.parse_args()

    meta = config_manager.MetadataManager()
    path_info = config_manager.PathManager()

    # check if core path exists
    if not path_info.check_core_path():
        print("Core files not found. Please reinstall the package or re-clone the repository.")
        return

    

    if args.version:
        print(meta.version)
    elif hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()