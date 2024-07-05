import os
import argparse


def parse_args(extra_args_provider=None, ignore_unknown_args=False):
    """

    Args:
        extra_args_provider (_type_, optional): _description_. Defaults to None.
        ignore_unknown_args (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """

    parser = argparse.ArgumentParser(description="Arguments", allow_abbrev=False)
    parser.add_argument("--metadata")

    # TODO: add groups
    parser = _add_count_matrix_path_args(parser)
    parser = _add_spatial_path_args(parser)
    parser = _add_cell2location_args(parser)

    # NOTE: arguments post-processing
    args = parser.parse_args()
    print(f"> jiaheng: we are parsing {args}")

    if args.count_matrix_h5ad is None:
        args.count_matrix_h5ad, _ = os.path.splitext(args.count_matrix)
        args.count_matrix_h5ad += ".h5ad"

    return args


def _add_count_matrix_path_args(parser):
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--count-matrix")
    group.add_argument("--count-matrix-h5ad")

    return parser


def _add_spatial_path_args(parser):
    return parser


def _add_cell2location_args(parser):
    group = parser.add_argument_group(title="cell2location")

    group.add_argument("--regression-model")

    return parser
