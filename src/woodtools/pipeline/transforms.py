import warnings
from pathlib import Path

import numpy as np
import torch
import torchvision.transforms as vtransforms
import zarr


def downsample(volume: np.ndarray, in_plane_target: int):
    if not volume.ndim == 4:
        raise ValueError(f'expecting 4D (C x D x H x W) images, got {volume.ndim}')
    C, D, H, W = volume.shape
    if C != 1:
        warnings.warn(f'encountered non-unit channel dimension: {C}')
    if not H == W:
        raise ValueError(f'in-plane dim mismatch: not square {H=} {W=}')
    
    factor = in_plane_target / H
    z_target = int(np.round(factor * D))
    target_size = tuple((z_target, in_plane_target, in_plane_target))
    
    downsampled_volume = torch.nn.functional.interpolate(
        torch.as_tensor(volume[np.newaxis, ...]), size=target_size, mode='trilinear'
    )
    return downsampled_volume[0, ...]


def downsample_zarr(
    source: Path,
    target: Path,
    in_plane_target: int
) -> Path:
    if target.exists():
        raise FileExistsError(f'cannot write to: \'{target}\': would overwrite existing')
    data = zarr.open(source)['downsampled/half']
    volume = data[...]
    ds_volume = downsample(volume, in_plane_target)
    out = zarr.open(target)
    out['downsampled/sam-native'] = np.asarray(ds_volume)
    return target


def datatransform(
    image: torch.Tensor | np.ndarray,
    angle: float,
    mode: str
) -> np.ndarray:
    assert image.ndim == 2, 'expecting planar image'
    image = image[np.newaxis, ...]
    mode = vtransforms.transforms.InterpolationMode(mode)
    image = torch.tensor(image)
    rotated_image = vtransforms.functional.rotate(
        image, angle=angle, interpolation=mode
    )
    image = np.squeeze(np.asarray(rotated_image))
    return image
    