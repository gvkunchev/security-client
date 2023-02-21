import sys

import qdarktheme
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtGui import QPixmap


class Gui:
    """Home security GUI."""

    MAP_SIZE = (600, 250)
    SENSOR_SIZE = 20
    SENSOR_ROUND = f"border-radius: {SENSOR_SIZE / 2}px;"
    SENSOR_GREEN = "border: 2px solid white; background: #3ef734;"
    SENSOR_RED = "border: 2px solid white; background: red;"
    SENSOR_COORDS = {
        'Bed room': (45, 168),
        'Kid room': (45, 100),
        'Front door': (212, 222),
    }

    def __init__(self, sensors_names, close_callback):
        """Initializator."""
        self._sensors_names = sensors_names
        self._sensors = {}
        self._close_callback = close_callback
        self._map = None
        self._app = QApplication([])
        self._main_window = QWidget()
        self._init_main_window()
        self._init_map()
        self._init_sensors()

    def _init_main_window(self):
        """Set up main window."""
        self._main_window.setWindowTitle("Home security")
        # TODO: switch the window size
        self._main_window.show()
        #self._main_window.showFullScreen()
    
    def _init_map(self):
        """Init home map."""
        # Create label with image as content
        self._map = QLabel(self._main_window)
        pixmap = QPixmap("images/map.png")
        self._map.resize(*self.MAP_SIZE)
        self._map.setPixmap(pixmap.scaled(self._map.size()))
        # Center the element
        window_width = self._main_window.frameGeometry().width()
        x_pos = (window_width - self.MAP_SIZE[0]) // 2
        self._map.move(x_pos, 50)
        self._map.show()
    
    def _init_sensors(self):
        """Init sensors."""
        for sensor_name in self._sensors_names:
            sensor = QLabel(self._main_window)
            x = self._map.pos().x() + self.SENSOR_COORDS[sensor_name][0]
            y = self._map.pos().y() + self.SENSOR_COORDS[sensor_name][1]
            sensor.move(x, y)
            sensor.resize(self.SENSOR_SIZE, self.SENSOR_SIZE)
            sensor.setStyleSheet(self.SENSOR_ROUND + self.SENSOR_GREEN)
            sensor.show()
            self._sensors[sensor_name] = sensor

    def run(self):
        """Run the app."""
        qdarktheme.setup_theme()
        self._app.exec()
        self._close_callback()
        sys.exit(0)
    
    def update_sensors(self, sensor_data):
        """Update sensors based on data."""
        for sensor in sensor_data:
            if sensor['state'] == 'Open':
                style = self.SENSOR_ROUND + self.SENSOR_RED
            else:
                style = self.SENSOR_ROUND + self.SENSOR_GREEN
            # Only force rerender if status is changed
            if style != self._sensors[sensor['location']].styleSheet():
                self._sensors[sensor['location']].setStyleSheet(style)
