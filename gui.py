"""Security client GUI."""

import os
import random
import sys

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QLine, QPoint


BASE_PATH = os.path.dirname(os.path.realpath(__file__))
IMAGES_PATH = os.path.join(BASE_PATH, 'images')

class PasswordWidget(QWidget):
    """Password prompt widget."""

    WINDOW_SIZE = (290, 290)
    POSITION_RANGE_X = (10, 400)
    POSITION_RANGE_Y = (10, 100)
    BUTTON_COUNT = 9
    BUTTON_SIZE = 70
    BUTTON_MARGIN = 20
    BUTTON_STYLE_DEF = ('background: white; border: 1px solid blue;'
                        'border-radius: 25px; font-size: 25px;')
    BUTTON_STYLE_SEL = ('background: #bac6ff; border: 1px solid blue;'
                        'border-radius: 25px; font-size: 25px;')
    LINE_THICKNESS = 10
    LINE_COLOR = Qt.blue

    def __init__(self, parent):
        """initializator."""
        self._mouse_path = []
        self._buttons = []
        self._lines = []
        self._callback = None
        super().__init__(parent)
        self.hide()
        self.setWindowFlags(Qt.CustomizeWindowHint)
        self.resize(*self.WINDOW_SIZE)
        self._populate_digits()

    def _populate_digits(self):
        """Populate the widget with digits."""
        for digit in range(self.BUTTON_COUNT):
            button = QLabel(str(digit + 1), self)
            button.resize(self.BUTTON_SIZE, self.BUTTON_SIZE)
            x_pos = self.BUTTON_MARGIN + (digit % 3) * (self.BUTTON_SIZE + self.BUTTON_MARGIN)
            y_pos = self.BUTTON_MARGIN + (digit // 3) * (self.BUTTON_SIZE + self.BUTTON_MARGIN)
            button.move(x_pos, y_pos)
            button.setStyleSheet(self.BUTTON_STYLE_DEF)
            button.setAlignment(Qt.AlignCenter)
            self._buttons.append(button)

    def _reset_buttons(self):
        """Reset buttons after pattern is selected."""
        for button in self._buttons:
            button.setStyleSheet(self.BUTTON_STYLE_DEF)
        self._lines = []
        self._mouse_path = None

    def paintEvent(self, event):
        """Paiting on the window."""
        painter = QPainter(self)
        pen = QPen(self.LINE_COLOR, self.LINE_THICKNESS)
        painter.setPen(pen)
        if len(self._lines) > 0:
            for line in self._lines:
                painter.drawLine(line)
        self.update()
        super().paintEvent(event)

    def show(self, callback):
        """Show the widget."""
        self._reset_buttons()
        self.move(random.randrange(*self.POSITION_RANGE_X),
                  random.randrange(*self.POSITION_RANGE_Y))
        self._callback = callback
        self.raise_()
        super().show()

    def mousePressEvent(self, event):
        """On mouse press."""
        if event.button() == Qt.LeftButton:
            self._mouse_path = []
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """On mouse release."""
        if event.button() == Qt.LeftButton:
            self.hide()
            self._callback(''.join(map(QLabel.text, self._mouse_path)))
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """On mouse move."""
        if self._mouse_path is not None:
            mouse_pos = event.pos()
            for button in self._buttons:
                button_pos = button.pos()
                if (mouse_pos.x() > button_pos.x() and
                    mouse_pos.y() > button_pos.y() and
                    mouse_pos.x() < button_pos.x() + self.BUTTON_SIZE and
                    mouse_pos.y() < button_pos.y() + self.BUTTON_SIZE):
                    if button not in self._mouse_path:
                        button.setStyleSheet(self.BUTTON_STYLE_SEL)
                        self._mouse_path.append(button)
                        if len(self._mouse_path) >= 2:
                            offset = QPoint(self.BUTTON_SIZE // 2,
                                            self.BUTTON_SIZE // 2)
                            start = self._mouse_path[-2].pos() + offset
                            end = self._mouse_path[-1].pos() + offset
                            self._lines.append(QLine(start, end))
        return super().mouseMoveEvent(event)


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
    SENSOR_YELLOW = "border: 2px solid white; background: yellow;"
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
        self._pass_window = PasswordWidget(self._main_window)
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
        #self._main_window.setCursor(Qt.BlankCursor) # TODO: Put this line back
        self._main_window.showFullScreen()

    def _init_map(self):
        """Init home map."""
        # Create label with image as content
        self._map = QLabel(self._main_window)
        pixmap = QPixmap(os.path.join(IMAGES_PATH, "map.png"))
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
        lock_pixmap = QPixmap(os.path.join(IMAGES_PATH, "locked.png"))
        self._lock.resize(*self.LOCK_SIZE)
        self._lock.setPixmap(lock_pixmap.scaled(self._lock.size()))
        self._lock.show()
        self._lock.move(x_pos, y_pos)
        self._lock.mousePressEvent = self._unarm_callback
        # Init unlock
        self._unlock = QLabel(self._main_window)
        unlock_pixmap = QPixmap(os.path.join(IMAGES_PATH, "unlocked.png"))
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
            elif sensor['state'] == 'Closed':
                style = self.SENSOR_ROUND + self.SENSOR_GREEN
            else:
                style = self.SENSOR_ROUND + self.SENSOR_YELLOW
            # Only force rerender if status is changed
            if style != self._sensors[sensor['location']].styleSheet():
                self._sensors[sensor['location']].setStyleSheet(style)

    def update_lock(self, arm_status):
        """Update lock based on data."""
        if arm_status['state'] == 'Unarmed':
            self._lock.hide()
            self._unlock.show()
        elif arm_status['state'] == 'Armed':
            self._unlock.hide()
            self._lock.show()
        else:
            self._unlock.hide()
            self._lock.hide()
    
    def get_pattern(self, callback):
        """Show pattern widget and return the result."""
        self._pass_window.show(callback)

