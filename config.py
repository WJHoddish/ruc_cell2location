from arguments import parse_args


_args = None


def get_args():
    global _args

    if _args is None:
        _args = parse_args()

    return _args
