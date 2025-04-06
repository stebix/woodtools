
import ipywidgets as widgets
import numpy as np
import torch
import torchvision.transforms as vtransforms

from IPython.display import display

from woodtools.pipeline.transforms import datatransform
from woodtools.pipeline.figure import ucl_figure

class RotationWidget:
    # Use these to sync to global variables 
    obj_name: str = '__CURRENT_OBJECT__'
    ID_key: str = 'ID'
    volume_key: str = 'volume'
    rotated_volume_key: str = 'rotated_volume'
        
    parameter_cache_name: str = '__PARAMETERS__'
    
    def __init__(
        self,
        volume: np.ndarray | None = None,
        vmin: float | None = None,
        vmax: float | None = None,
        figsize: tuple[float, float] = (18, 6),
        ID: str | None = None,
        alpha_range: tuple[float, float] = (-20.0, 20.0)
    ) -> None:
        self.volume = self.deduce_volume() if volume is None else volume
        self.vmin = vmin
        self.vmax = vmax
        self.figsize = figsize
        self.ID = ID or self.deduce_ID()
        
        self.fig, self.axes, self.mapping = ucl_figure(
            self.volume, vmin=self.vmin, vmax=self.vmax, figsize=self.figsize, ID=self.ID
        )
        
        alpha_min, alpha_max = alpha_range
        self.angle_slider = widgets.FloatSlider(
            value=0, min=alpha_min, max=alpha_max, step=0.1, desc='Angle Slider [deg]'
        )
        self.rotate_button = widgets.Button(description='Rotate', icon='gear')
        self.interpolation_dropdown = widgets.Dropdown(options=['nearest', 'bilinear'])
        
        self.setup_widgets()
        
        
    def deduce_ID(self) -> str:
        return globals()[self.obj_name][self.ID_key]
    
    def deduce_volume(self) -> np.ndarray:
        return globals()[self.obj_name][self.volume_key]
    
    def _callback(self, change):
        angle = change['new']
        for name, items in self.mapping.items():
            ax = items['ax']
            data = items['data']
            transformed_data = datatransform(data, angle=angle, mode='nearest')
            items['image'].set_data(transformed_data)

        self.fig.suptitle(f'Angle: {angle:.2f} deg')
        self.fig.canvas.draw_idle()
        return
    
    def get_interpolation_mode(self) -> vtransforms.InterpolationMode:
        return vtransforms.InterpolationMode(self.interpolation_dropdown.value)
    
    def rotate(self, *args, **kwargs):
        volume = torch.as_tensor(self.volume)
        angle = self.angle_slider.value
        mode = self.get_interpolation_mode()
        rotated_volume = vtransforms.functional.rotate(
            volume, angle=angle, interpolation=mode
        )
        globals()[self.obj_name][self.rotated_volume_key] = rotated_volume
        try:
            globals()[self.parameter_cache_name][self.ID]['rotation'] = {
                'angle' : angle, 'mode' : str(mode)
            }
        except KeyError:
            globals()[self.parameter_cache_name][self.ID] = {}
            globals()[self.parameter_cache_name][self.ID]['rotation'] = {
                'angle' : angle, 'mode' : str(mode)
            }
    
    def setup_widgets(self):
        self.angle_slider.observe(self._callback, names='value')
        self.rotate_button.on_click(self.rotate)
        display(widgets.HBox([self.angle_slider, self.rotate_button]))