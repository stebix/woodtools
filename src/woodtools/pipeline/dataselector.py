import zarr
from pathlib import Path
from typing import Callable, Sequence
import ipywidgets as widgets

class DatasetSelectorWidget:
    
    STORAGE_VARIABLE_NAME: str = '__CURRENT_OBJECT__'
    volume_name: str = 'volume'
    ID_name: str = 'ID'
    
    def __init__(
        self,
        classes: Sequence[str],
        subidentifiers: Sequence[str],
        basepath: Path
    ) -> None:
        self.classes = classes
        self.subidentifiers = subidentifiers
        self.basepath = basepath
        
        self.class_selector = widgets.Dropdown(options=self.classes, desc='Class Selection')
        self.subid_selector = widgets.Dropdown(options=self.subidentifiers, desc='Sub ID Selection')
        self.load_button = widgets.Button(description='Load', icon='database')
        
        self.setup_widgets()

        
    def build_path(self, class_: str, subidentifier: str) -> Path:
        return self.basepath / f'{class_}-{subidentifier}.zarr'
    

    def load_file(self, *args, **kwargs):
        path = self.build_path(self.class_selector.value, self.subid_selector.value)
        # This is evil global variable stuff >:[]
        zarrfile = zarr.open(path, mode='r')
        volume = zarrfile['metric/raw'][...]
        ID = f'{self.class_selector.value}-{self.subid_selector.value}'
        globals()[self.STORAGE_VARIABLE_NAME][self.volume_name] = volume
        globals()[self.STORAGE_VARIABLE_NAME][self.ID_name] = ID


    def setup_widgets(self):
        self.load_button.on_click(self.load_file)
    