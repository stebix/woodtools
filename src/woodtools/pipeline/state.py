from copy import deepcopy

import numpy as np
import attrs


@attrs.define
class WorkItem:
    ID: str | None = None
    volume: np.ndarray | None = None
    parameters: dict = attrs.field(factory=dict)

    def copy(self) -> 'WorkItem':
        """
        Create a copy of the current WorkItem instance.
        """
        return WorkItem(
            ID=self.ID,
            volume=self.volume.copy() if self.volume is not None else None,
            parameters=deepcopy(self.parameters)
        )
    

    def __repr__(self):
        """
        Custom string representation of the WorkItem instance.
        """
        volume_info = f'(volume={self.volume.shape}, {self.volume.dtype})' if self.volume is not None else '(volume=None)'
        return f'WorkItem(ID={self.ID}, {volume_info}, parameters={self.parameters})'
    

    def __str__(self):
        """
        Custom string representation of the WorkItem instance.
        """
        return self.__repr__()


class StateManager:
    """
    Manage the state across multiple widgets.
    """
    def __init__(
        self,
        initial_item: WorkItem = WorkItem(),
    ) -> None:
        self.item = initial_item
        self.observers: list = []

    def update(self, new_item: WorkItem) -> None:
        self.item = new_item
        self.notify_observers()
    
    def register_observer(self, observer) -> None:
        # Register an observer to be notified on state changes
        self.observers.append(observer)

    def notify_observers(self) -> None:
        # Notify observers about the state change
        for observer in self.observers:
            observer.on_state_change()