from collections.abc import Sequence
from typing import NamedTuple

import matplotlib.pyplot as plt
import numpy as np
import ipywidgets as widgets

from IPython.display import display
from matplotlib.widgets import RectangleSelector


class SynchronizedRectangleSelector:
    obj_name: str = '__CURRENT_OBJECT__'
    volume_key: str = 'rotated_volume'
    ID_key: str = 'ID'
    parameters_key: str = '__PARAMETERS__'
        
    def __init__(self, images=None, num_axes=3):
        """
        Initialize a figure with multiple axes and synchronized rectangle selectors
        
        Parameters:
        -----------
        images : list of numpy.ndarray, optional
            List of images to display. If None, sample images will be created.
        num_axes : int, default=3
            Number of axes to create if images is None
        """
        # Create sample images if none provided
        if images is None:
            self.images = self.deduce_images()
            num_axes = len(self.images)
            
        else:
            self.images = images
            num_axes = len(images)
        
        # Create figure and axes
        self.fig, self.axes = plt.subplots(1, num_axes, figsize=(15, 5))
        if num_axes == 1:
            self.axes = [self.axes]  # Make it a list for consistent indexing
        
        # Initialize rectangle coordinates
        self.rect_coords = {'x0': 0, 'y0': 0, 'x1': 0, 'y1': 0}
        
        # Display images and create selectors
        self.img_plots = []
        self.selectors = []
        
        for i, ax in enumerate(self.axes):
            img_plot = ax.imshow(self.images[i], cmap='viridis')
            self.img_plots.append(img_plot)
            
            # Create rectangle selector for each axis
            rs = RectangleSelector(
                ax, self.line_select_callback,
                useblit=True,
                button=[1],  # Left mouse button only
                minspanx=5, minspany=5,
                spancoords='pixels',
                interactive=True,
                props=dict(facecolor='red', edgecolor='yellow', alpha=0.3, fill=True)
            )
            self.selectors.append(rs)
            
            # Add title
            ax.set_title(f'Image {i+1}')
        
        # Setup widgets
        self.setup_widgets()
        
        # Show the plot
        plt.tight_layout()
        
    def deduce_images(self) -> np.ndarray:
        volume = globals()[self.obj_name][self.volume_key]
        uidx, cidx, lidx = 0, volume.shape[0] //2, volume.shape[0] - 1
        images = [volume[idx, ...] for idx in (uidx, cidx, lidx)]
        return images
    
    def deduce_ID(self) -> str:
        return globals()[self.obj_name][self.ID_key]
    
    def line_select_callback(self, eclick, erelease):
        """Callback for rectangle selector"""
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        
        # Update the coordinates
        self.rect_coords = {'x0': x1, 'y0': y1, 'x1': x2, 'y1': y2}
        
        # Update all selectors to the same position
        self.sync_all_selectors()
        
        # Update the coordinate display
        self.update_coord_text()
    
    def sync_all_selectors(self):
        """Synchronize all selectors to the current rectangle coordinates"""
        for rs in self.selectors:
            # Disable callback temporarily to avoid recursion
            prev_onselect = rs.onselect
            rs.onselect = None
            
            # Update the selector position
            # Note: we need to convert between data and display coordinates
            rs.extents = (
                self.rect_coords['x0'],
                self.rect_coords['x1'],
                self.rect_coords['y0'],
                self.rect_coords['y1']
            )
            
            # Restore callback
            rs.onselect = prev_onselect
            
            # Redraw
            rs.update()
    
    def set_rectangle_position(self, x0, y0, x1, y1):
        """
        Programmatically set the position of the rectangle selector on all axes
        
        Parameters:
        -----------
        x0, y0 : float
            Coordinates of the top-left corner
        x1, y1 : float
            Coordinates of the bottom-right corner
        """
        self.rect_coords = {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1}
        self.sync_all_selectors()
        self.update_coord_text()
        self.fig.canvas.draw_idle()
    
    def update_coord_text(self):
        """Update the text of the coordinate display"""
        self.coord_text.value = f"""
        <b>Current dataset:</b><br>
        ID = {self.deduce_ID()}<br>
        <b>Selected Rectangle Coordinates:</b><br>
        Top-left: ({self.rect_coords['x0']:.2f}, {self.rect_coords['y0']:.2f})<br>
        Bottom-right: ({self.rect_coords['x1']:.2f}, {self.rect_coords['y1']:.2f})<br>
        Width: {abs(self.rect_coords['x1'] - self.rect_coords['x0']):.2f}<br>
        Height: {abs(self.rect_coords['y1'] - self.rect_coords['y0']):.2f}
        """
    
    def export_coordinates(self, b):
        """Export the coordinates to a file"""
        # Create a dictionary with the coordinates
        coords_dict = {
            'top_left': [float(self.rect_coords['x0']), float(self.rect_coords['y0'])],
            'top_right': [float(self.rect_coords['x1']), float(self.rect_coords['y0'])],
            'bottom_left': [float(self.rect_coords['x0']), float(self.rect_coords['y1'])],
            'bottom_right': [float(self.rect_coords['x1']), float(self.rect_coords['y1'])]
        }
        ID = self.deduce_ID()
        try:
            globals()[self.parameters_key][ID]['roi'] = coords_dict
        except KeyError:
            globals()[self.parameters_key][ID] = {}
            globals()[self.parameters_key][ID]['roi'] = coords_dict
    
    def setup_widgets(self):
        """Set up the ipywidgets for user interaction"""
        # Create a text widget to display coordinates
        self.coord_text = widgets.HTML(
            value=f"""
            <b>Current dataset:</b><br>
            ID = {self.deduce_ID()}<br>
            <b>Selected Rectangle Coordinates:</b><br>
            <b>Selected Rectangle Coordinates:</b><br>No selection yet
            """,
            layout=widgets.Layout(width='100%')
        )
        
   
        # Create an export button
        self.export_button = widgets.Button(
            description='Export Coordinates',
            button_style='success',
            tooltip='Click to export the coordinates'
        )
        self.export_button.on_click(self.export_coordinates)
        
        # Display all widgets
        display(widgets.HBox([self.coord_text, self.export_button]))
    


# Example usage
def run_synchronized_selector(images=None, num_axes=3):
    """
    Run the synchronized rectangle selector tool
    
    Parameters:
    -----------
    images : list of numpy.ndarray, optional
        List of images to display. If None, sample images will be created.
    num_axes : int, default=3
        Number of axes to create if images is None
    
    Returns:
    --------
    SynchronizedRectangleSelector
        The annotation tool instance
    """
    tool = SynchronizedRectangleSelector(images, num_axes)
    return tool


class Point(NamedTuple):
    x: float
    y: float



def extract_roi(volume: np.ndarray, roispec: dict[str, Sequence[float]]) -> np.ndarray:
    """
    Extract the subvolume that is specified by the roispec.
    Along the first z-axis, all slices are chosen.
    Returns a copy to avoid mutation of the source array.
    
    Parameters
    ----------
    
    volume : np.ndarray
        The source volume from which the data is extracted.
        
    roispec : Mapping[str, Sequence[float]]
        Specification of the region-of-interest.
        Shoudl be given as a mapping of point names
        {'top_left', 'top_right', 'bottom_left', 'bottom_right'}
        to sequences of length 2 of coordinates.
        
    Returns
    -------
    
    subvolume : np.ndarray
        The subvolume selected by the roispec.    
    
    Notes
    -----
    
    Point scheme
    p0 --- p1
    |      |
    p2 --- p3
    """
    p0 = Point(*roispec['top_left'])
    p1 = Point(*roispec['top_right'])
    p2 = Point(*roispec['bottom_left'])
    p3 = Point(*roispec['bottom_right'])

    dx = int(np.round(p1.x - p0.x))
    assert np.isclose(dx, int(np.round(p3.x - p2.x)))
    dy = int(np.round(p2.y - p0.y))
    assert np.isclose(dy, int(np.round(p3.y - p1.y)))
    x0 = int(np.round(p0.x))
    y0 = int(np.round(p0.y))
    
    slices = tuple(
        (slice(None), slice(y0, y0+dy), slice(x0, x0+dx))
    )
    return np.copy(volume[*slices])
    
    