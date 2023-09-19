import argparse
import logging
from actions.parse import parse

def main(args: argparse.Namespace) -> None:
    result = parse(args.filepath)
    logging.info('Result: %s', result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='path to the file or directory to be processed')
    parser.add_argument('-v', '--verbose', action='store_true', help='increase output verbosity')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    main(args)