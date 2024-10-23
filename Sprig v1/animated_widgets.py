from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, Qt


class SlidingStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_direction = Qt.Orientation.Horizontal
        self.m_speed = 500
        self.m_animationtype = QEasingCurve.Type.OutCubic
        self.m_now = 0
        self.m_next = 0
        self.m_wrap = False
        self.m_pnow = QPoint(0, 0)
        self.m_active = False

    def setDirection(self, direction):
        self.m_direction = direction

    def slideIn(self, index):
        if self.m_active:
            return

        self.m_active = True

        width = self.frameRect().width()
        height = self.frameRect().height()

        # Set next index and direction
        self.m_next = index

        if self.m_now == self.m_next:
            self.m_active = False
            return

        offsetx = width
        offsety = 0
        self.widget(self.m_next).setGeometry(0, 0, width, height)

        if self.m_now < self.m_next:
            offsetx = width
        else:
            offsetx = -width

        curr_pos = self.widget(self.m_now).pos()
        next_pos = self.widget(self.m_next).pos()
        self.m_pnow = curr_pos

        offset = QPoint(offsetx, offsety)
        self.widget(self.m_next).move(next_pos + offset)
        self.widget(self.m_next).show()
        self.widget(self.m_next).raise_()

        anim_group_now = QPropertyAnimation(
            self.widget(self.m_now), b"pos", self)
        anim_group_now.setDuration(self.m_speed)
        anim_group_now.setEasingCurve(self.m_animationtype)
        anim_group_now.setStartValue(curr_pos)
        anim_group_now.setEndValue(curr_pos - offset)

        anim_group_next = QPropertyAnimation(
            self.widget(self.m_next), b"pos", self)
        anim_group_next.setDuration(self.m_speed)
        anim_group_next.setEasingCurve(self.m_animationtype)
        anim_group_next.setStartValue(next_pos + offset)
        anim_group_next.setEndValue(next_pos)

        anim_group_now.finished.connect(self._animation_finished)

        anim_group_now.start()
        anim_group_next.start()

    def _animation_finished(self):
        self.widget(self.m_now).hide()
        self.widget(self.m_now).move(self.m_pnow)
        self.m_now = self.m_next
        self.m_active = False
