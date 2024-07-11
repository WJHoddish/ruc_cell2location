import os
import time

import pandas as pd
import anndata as ad

from anndata import AnnData


def print_time(start, msg):
    print(f"Running time ({msg}): {str(round((time.time() - start) / 60, 4))} min")


def find_longest_common_substring(strs):
    if not strs:
        return ""

    # 取第一个字符串作为基准
    s1 = strs[0]
    common_substr = ""

    for i in range(len(s1)):
        for j in range(i + 1, len(s1) + 1):
            substr = s1[i:j]
            if all(substr in s for s in strs) and len(substr) > len(common_substr):
                common_substr = substr

    return common_substr
