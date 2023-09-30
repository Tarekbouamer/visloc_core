import argparse


def size_list(string):
    try:
        return int(string)
    except ValueError:
        try:
            return [int(item) for item in string.replace(" ", "").split(',')]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid input: '{string}'")