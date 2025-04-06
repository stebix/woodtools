from pathlib import Path
from typing import Sequence

import ipywidgets as widgets
import zarr

from IPython.display import display

from woodtools.pipeline.state import WorkItem, StateManager


class DatasetSelectorWidget:
    
    STORAGE_VARIABLE_NAME: str = '__CURRENT_OBJECT__'
    volume_name: str = 'volume'
    ID_name: str = 'ID'
    
    def __init__(
        self,
        state_manager: StateManager,
        basepath: Path,
        classes: Sequence[str] = ('acer', 'pinus'),
        subidentifiers: Sequence[str] = ('center', 'left', 'right', 'upper', 'lower'),
    ) -> None:
        
        self.state_manager = state_manager
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

        work_item = WorkItem(ID=ID, volume=volume)
        self.state_manager.update(work_item)


    def setup_widgets(self):
        self.load_button.on_click(self.load_file)
        display(widgets.HBox([self.class_selector, self.subid_selector, self.load_button]))
    