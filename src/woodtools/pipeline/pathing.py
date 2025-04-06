from collections import OrderedDict
from collections.abc import Callable, Sequence
from pathlib import Path

import numpy as np
import skimage.io

def generate_path_mapping(
    paths: Sequence[Path],
    match_fun: Callable[[str], tuple[bool, int | None]]
) -> OrderedDict[int, Path]:
    path_mapping = OrderedDict()
    for path in paths:
        is_match, ID = match_fun(path.stem)
        if not is_match:
            continue
        path_mapping[ID] = path
    return path_mapping


def assemble_array(
    path_mapping: OrderedDict
) -> np.ndarray:
    slices = [
        skimage.io.imread(p) for _, p in sorted(path_mapping.items())
    ]
    return np.stack(slices, axis=0)