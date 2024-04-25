import math
from PyQt6.QtCore import QVariantAnimation
from PyQt6.QtWidgets import QPushButton
from fileBar import FILE_WORKER


class AddButton(QPushButton):
    addButtonStyleTemplate = """
        QPushButton {{
            border: none;
            border-radius: 37px;
            font-weight: bold;
            font-size: 25px;
            color: white;
            background: qlineargradient(x1:{start_x}, y1:{start_y}, x2:{end_x}, y2:{end_y},
                                stop:0 rgba(57, 128, 233, 255),
                                stop:1 rgba(0, 255, 68, 255));
        }}
        QPushButton:hover {{
            color: black;
        }}
        QPushButton:pressed {{
            color: gray;
        }}
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setText("+")
        self.setFixedSize(75, 75)
        self._angle = 0
        self.setStyleSheet(self._generate_style())

        self.animation = QVariantAnimation()
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setDuration(4000)
        self.animation.setLoopCount(-1)  # set infinite animation
        self.animation.valueChanged.connect(self._update_gradient)
        self.animation.start()
    
    def _update_gradient(self, angle):
        self._angle = angle
        self.setStyleSheet(self._generate_style())
    
    def _generate_style(self):
        start_x = 0.5 + 0.5 * math.cos(math.radians(self._angle))
        start_y = 0.5 + 0.5 * math.sin(math.radians(self._angle))
        end_x = 0.5 + 0.5 * math.cos(math.radians(self._angle + 180))
        end_y = 0.5 + 0.5 * math.sin(math.radians(self._angle + 180))
        return self.addButtonStyleTemplate.format(start_x=start_x, start_y=start_y, end_x=end_x, end_y=end_y)
