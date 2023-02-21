from threading import Timer

from api import Api
from gui import Gui


class Security:
    """Security controller."""

    SENSORS = ['Bed room', 'Kid room', 'Front door']
    TIME_DELTA = 1 # Time between server sensor checks 

    def __init__(self):
        """Initializator."""
        self._running = True
        self._api = Api()
        self._gui = Gui(self.SENSORS, self.on_exit, self.on_arm, self.on_unarm)
        self._monitor_server()
        self._gui.run()

    def _monitor_server(self):
        """Monitor sensors."""
        if self._running:
            Timer(self.TIME_DELTA, self._monitor_server).start()
        self._gui.update_sensors(self._api.get_sensors_data())
        self._gui.update_lock(self._api.get_arm_data())
    
    def on_arm(self, _):
        """On clicking the lock to arm home."""
        self._api.arm()
        self._gui.update_lock(self._api.get_arm_data())
    
    def on_unarm(self, _):
        """On clicking the lock to unarm home."""
        # TODO: verify password
        self._api.unarm()
        self._gui.update_lock(self._api.get_arm_data())

    def on_exit(self):
        """On exit"""
        self._running = False

if __name__ == '__main__':
    Security()
