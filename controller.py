from gui import Gui


class Security:
    """Security controller."""

    SENSORS = ['Bed room', 'Kid room', 'Front door']

    def __init__(self):
        """Initializator."""
        self._sensors = self.SENSORS[:]
        self._gui = Gui(self._sensors)
        

if __name__ == '__main__':
    Security()