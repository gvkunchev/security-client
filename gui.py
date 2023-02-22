"""Security client GUI."""

import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Gui:
    """Home security GUI."""

    WINDOW_WIDTH = 800
    MAIN_STYLE = "background-color: #28382c;"
    LOCK_SIZE = (100, 100)
    MAP_SIZE = (600, 250)
    MAP_MARGIN = 50
    SENSOR_SIZE = 20
    SENSOR_ROUND = f"border-radius: {SENSOR_SIZE / 2}px;"
    SENSOR_GREEN = "border: 2px solid white; background: #3ef734;"
    SENSOR_RED = "border: 2px solid white; background: red;"
    SENSOR_COORDS = {
        'Bed room': (45, 168),
        'Kid room': (45, 100),
        'Front door': (212, 222),
    }

    def __init__(self, sensors_names,
                 close_callback, arm_callback, unarm_callback):
        """Initializator."""
        self._sensors_names = sensors_names
        self._sensors = {}
        self._close_callback = close_callback
        self._arm_callback = arm_callback
        self._unarm_callback = unarm_callback
        self._map = None
        self._lock = None
        self._unlock = None
        self._app = QApplication([])
        self._main_window = QWidget()
        self._init_main_window()
        self._init_map()
        self._init_locks()
        self._init_sensors()

    def get_window_width(self):
        """Get window width."""
        return self.WINDOW_WIDTH
        # The line below produces wrong result on the Pi display
        # so instead of using it, the value is hardcoded.
        return self._main_window.frameGeometry().width()

    def _init_main_window(self):
        """Set up main window."""
        self._main_window.setWindowTitle("Home security")
        self._main_window.setStyleSheet(self.MAIN_STYLE)
        #self._main_window.setCursor(Qt.BlankCursor) # TODO: Put back
        self._main_window.showFullScreen()

    def _init_map(self):
        """Init home map."""
        # Create label with image as content
        self._map = QLabel(self._main_window)
        pixmap = QPixmap("images/map.png")
        self._map.resize(*self.MAP_SIZE)
        self._map.setPixmap(pixmap.scaled(self._map.size()))
        # Center the element
        window_width = self.get_window_width()
        x_pos = (window_width - self.MAP_SIZE[0]) // 2
        self._map.move(x_pos, self.MAP_MARGIN)
        self._map.show()

    def _init_locks(self):
        """Init locks."""
        # Calculate position
        window_width = self.get_window_width()
        x_pos = (window_width - self.LOCK_SIZE[0]) // 2
        y_pos = self._map.frameGeometry().height() + self.MAP_MARGIN*2
        # Init lock
        self._lock = QLabel(self._main_window)
        lock_pixmap = QPixmap("images/locked.png")
        self._lock.resize(*self.LOCK_SIZE)
        self._lock.setPixmap(lock_pixmap.scaled(self._lock.size()))
        self._lock.show()
        self._lock.move(x_pos, y_pos)
        self._lock.mousePressEvent = self._unarm_callback
        # Init unlock
        self._unlock = QLabel(self._main_window)
        unlock_pixmap = QPixmap("images/unlocked.png")
        self._unlock.resize(*self.LOCK_SIZE)
        self._unlock.setPixmap(unlock_pixmap.scaled(self._unlock.size()))
        self._unlock.show()
        self._unlock.move(x_pos, y_pos)
        self._unlock.mousePressEvent = self._arm_callback

    def _init_sensors(self):
        """Init sensors."""
        for sensor_name in self._sensors_names:
            sensor = QLabel(self._main_window)
            x_pos = self._map.pos().x() + self.SENSOR_COORDS[sensor_name][0]
            y_pos = self._map.pos().y() + self.SENSOR_COORDS[sensor_name][1]
            sensor.move(x_pos, y_pos)
            sensor.resize(self.SENSOR_SIZE, self.SENSOR_SIZE)
            sensor.setStyleSheet(self.SENSOR_ROUND + self.SENSOR_GREEN)
            sensor.show()
            self._sensors[sensor_name] = sensor

    def run(self):
        """Run the app."""
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

    def update_lock(self, arm_status):
        """Update lock based on data."""
        if arm_status['state'] == 'Unarmed':
            self._lock.hide()
            self._unlock.setGraphicsEffect(None)
            self._unlock.show()
        else:
            self._unlock.hide()
            self._lock.setGraphicsEffect(None)
            self._lock.show()
