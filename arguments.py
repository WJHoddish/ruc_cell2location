import os
import argparse


def parse_args(extra_args_provider=None, ignore_unknown_args=False):
    """_summary_

    Args:
        extra_args_provider (_type_, optional): _description_. Defaults to None.
        ignore_unknown_args (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """

    parser = argparse.ArgumentParser(description="Arguments", allow_abbrev=False)

    # TODO (jiaheng):
    parser = _add_file_path_args(parser)

    args = parser.parse_args()

    # TODO (jiaheng): come up with new global vars
    file_path, _ = os.path.splitext(args.count)
    setattr(args, "file_path", file_path + ".h5ad")

    return args


def _add_file_path_args(parser):
    group = parser.add_argument_group(title="single cell, spatial data")

    group.add_argument(
        "--count",
        default="~/Data/ESCC_LDX.count.tsv",
    )
    group.add_argument(
        "--metadata",
        default="~/Data/ESCC_LDX.metadata.tsv",
    )

    return parser
