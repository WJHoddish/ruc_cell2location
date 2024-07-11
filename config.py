from arguments import parse_args


_args = None


def get_args():
    global _args

    if _args is None:
        _args = parse_args()

    return _args


patients = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10"]
stages = ["pre", "post"]


packages = {
    "cell2location": {
        "path": "/work/wangjh/csv",
        "prefix": "",
        "surfix": "_q05_result.csv",
    },
}
