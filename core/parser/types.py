import argparse

def int_list(string, sep=','):
    """Convert a string to a list of integers. used to parse list int arguments"""
    try:
        return int(string)
    except ValueError:
        try:
            return [int(item) for item in string.replace(" ", "").split(sep)]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid input: '{string}'")
        
def float_list(string, sep=','):
    """Convert a string to a list of floats. used to parse list float arguments"""
    try:
        return float(string)
    except ValueError:
        try:
            return [float(item) for item in string.replace(" ", "").split(sep)]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid input: '{string}'")