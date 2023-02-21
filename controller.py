from threading import Timer

from api import Api
from gui import Gui


class Security:
    """Security controller."""

    SENSORS = ['Bed room', 'Kid room', 'Front door']
    TIME_DELTA = 0.3 # Time between server sensor checks 

    def __init__(self):
        """Initializator."""
        self._running = True
        self._api = Api()
        self._gui = Gui(self.SENSORS, self.on_exit)
        self._monitor_sensors()
        self._gui.run()

    def _monitor_sensors(self):
        """Monitor sensors."""
        if self._running:
            Timer(self.TIME_DELTA, self._monitor_sensors).start()
        self._gui.update_sensors(self._api.get_sensors_data())

    def on_exit(self):
        """On exit"""
        self._running = False

if __name__ == '__main__':
    Security()