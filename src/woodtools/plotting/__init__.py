import matplotlib.pyplot as plt
import numpy as np

def ucl_figure(
    volume: np.ndarray,
    vmin=None,
    vmax=None,
    figsize: tuple[float, float] = (12, 3),
    ID: str = ''
) -> tuple:
    D, H, W = volume.shape
    uidx, cidx, lidx = 0, D //2, D - 1
    fig, axes = plt.subplots(ncols=3, figsize=figsize)
    
    upper_slc = volume[uidx, ...]
    center_slc = volume[cidx, ...]
    lower_slc = volume[lidx, ...]
    
    mapping = {
        'upper' : {'ax' : axes[0], 'index' : uidx, 'data' : upper_slc},
        'center' : {'ax' : axes[1], 'index' : cidx, 'data' : center_slc},
        'lower' : {'ax' : axes[2], 'index' : lidx, 'data' : lower_slc},
    }
    
    for name, items in mapping.items():
        ax = items['ax']
        data = items['data']
        index = items['index']
        title = f'{name} @ {index}'
        
        img = ax.imshow(data, vmin=vmin, vmax=vmax)
        ax.set_title(title)
        items['image'] = img
    
    ax.text(0.125, 0.93, s=f'ID = {ID}', transform=fig.transFigure, ha='left', va='top')
    
    fig.suptitle('Angle: 0 deg')
    fig.tight_layout()
    return (fig, axes, mapping)