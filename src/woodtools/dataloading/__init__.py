from pathlib import Path
import numpy as np

import zarr


def load_volume(source: Path) -> np.ndarray:
    volume = zarr.open(source)['downsampled/sam-native'][...]
    volume = np.squeeze(volume)
    assert volume.ndim == 3, f'expected ndim == 3, got {volume.ndim}'
    return volume