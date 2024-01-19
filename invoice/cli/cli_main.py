from invoice.cli import cli_parser
from invoice.core.info import Meta_info


def main():
    parser = cli_parser.build_parser()
    args = parser.parse_args()

    meta = Meta_info()

    if args.version:
        print(meta.version)
    elif hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()