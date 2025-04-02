import sys
import asyncio
import logging
import math
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QDialog, QLabel
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QFont, QRadialGradient, QLinearGradient, QCursor, QPainterPath
from PyQt6.QtCore import Qt, QTimer, QPoint, QPropertyAnimation, QEasingCurve, QRect, QSize, pyqtProperty
from app.agent.manus import Manus  # Keeping the original import
from app.logger import logger  # Keeping the original import

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModernInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chat with Cat")
        self.setGeometry(100, 100, 400, 150)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f4f8;
                border-radius: 10px;
                border: 1px solid #d0d7de;
            }
            QLineEdit {
                padding: 12px;
                border-radius: 6px;
                border: 1px solid #d0d7de;
                background-color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2ea44f;
                color: white;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #2c974b;
            }
            QLabel {
                font-size: 14px;
                color: #24292f;
                font-weight: bold;
            }
        """)
        
        self.layout = QVBoxLayout()
        
        self.title_label = QLabel("Talk to your cat!")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Enter your prompt (or 'exit'/'quit' to quit)")
        self.send_button = QPushButton("Send")
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.clicked.connect(self.accept)
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.prompt_input)
        self.layout.addWidget(self.send_button)
        self.setLayout(self.layout)
        
        # Set focus to input field
        self.prompt_input.setFocus()

class AnimatedPet(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._eye_size = 10
        self._blink_state = 0
        self._mouth_curve = 0
        self._body_scale = 1.0
        self._head_rotation = 0
        self._tail_angle = 0
        self._pepper_bounce = 0
        
        # Setup animations
        self.setup_animations()

    def setup_animations(self):
        # Blinking animation
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink)
        self.blink_timer.start(3000)  # Blink every 3 seconds
        
        # Breathing animation
        self.breath_anim = QPropertyAnimation(self, b"body_scale")
        self.breath_anim.setDuration(2000)
        self.breath_anim.setStartValue(1.0)
        self.breath_anim.setEndValue(1.05)
        self.breath_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.breath_anim.setLoopCount(-1)  # Infinite loop
        self.breath_anim.setDirection(QPropertyAnimation.Direction.Forward)
        self.breath_anim.start()
        
        # Head movement animation
        self.head_anim = QPropertyAnimation(self, b"head_rotation")
        self.head_anim.setDuration(5000)
        self.head_anim.setStartValue(-3)
        self.head_anim.setEndValue(3)
        self.head_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.head_anim.setLoopCount(-1)  # Infinite loop
        self.head_anim.setDirection(QPropertyAnimation.Direction.Forward)
        self.head_anim.start()
        
        # Mouth animation
        self.mouth_anim = QPropertyAnimation(self, b"mouth_curve")
        self.mouth_anim.setDuration(4000)
        self.mouth_anim.setStartValue(0)
        self.mouth_anim.setEndValue(10)
        self.mouth_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.mouth_anim.setLoopCount(-1)  # Infinite loop
        self.mouth_anim.setDirection(QPropertyAnimation.Direction.Forward)
        self.mouth_anim.start()
        
        # Tail animation
        self.tail_anim = QPropertyAnimation(self, b"tail_angle")
        self.tail_anim.setDuration(3000)
        self.tail_anim.setStartValue(-15)
        self.tail_anim.setEndValue(15)
        self.tail_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.tail_anim.setLoopCount(-1)  # Infinite loop
        self.tail_anim.setDirection(QPropertyAnimation.Direction.Forward)
        self.tail_anim.start()
        
        # Pepper bounce animation
        self.pepper_anim = QPropertyAnimation(self, b"pepper_bounce")
        self.pepper_anim.setDuration(1500)
        self.pepper_anim.setStartValue(0)
        self.pepper_anim.setEndValue(5)
        self.pepper_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.pepper_anim.setLoopCount(-1)  # Infinite loop
        self.pepper_anim.setDirection(QPropertyAnimation.Direction.Forward)
        self.pepper_anim.start()
    
    def blink(self):
        # Start a quick blink animation
        blink_anim = QPropertyAnimation(self, b"eye_size")
        blink_anim.setDuration(200)
        blink_anim.setStartValue(10)
        blink_anim.setEndValue(1)
        blink_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        # And open eyes again
        blink_anim2 = QPropertyAnimation(self, b"eye_size")
        blink_anim2.setDuration(200)
        blink_anim2.setStartValue(1)
        blink_anim2.setEndValue(10)
        blink_anim2.setEasingCurve(QEasingCurve.Type.InOutQuad)
        
        blink_anim.finished.connect(blink_anim2.start)
        blink_anim.start()
    
    # Define properties for animations
    @pyqtProperty(float)
    def eye_size(self):
        return self._eye_size
    
    @eye_size.setter
    def eye_size(self, size):
        self._eye_size = size
        self.update()
    
    @pyqtProperty(float)
    def body_scale(self):
        return self._body_scale
    
    @body_scale.setter
    def body_scale(self, scale):
        self._body_scale = scale
        self.update()
    
    @pyqtProperty(float)
    def head_rotation(self):
        return self._head_rotation
    
    @head_rotation.setter
    def head_rotation(self, rotation):
        self._head_rotation = rotation
        self.update()
    
    @pyqtProperty(float)
    def mouth_curve(self):
        return self._mouth_curve
    
    @mouth_curve.setter
    def mouth_curve(self, curve):
        self._mouth_curve = curve
        self.update()
    
    @pyqtProperty(float)
    def tail_angle(self):
        return self._tail_angle
    
    @tail_angle.setter
    def tail_angle(self, angle):
        self._tail_angle = angle
        self.update()
    
    @pyqtProperty(float)
    def pepper_bounce(self):
        return self._pepper_bounce
    
    @pepper_bounce.setter
    def pepper_bounce(self, bounce):
        self._pepper_bounce = bounce
        self.update()

class DesktopPet(AnimatedPet):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            self.windowFlags() |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool  # Prevents showing in taskbar
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle("Desktop Cat")
        self.setGeometry(100, 100, 250, 350)
        
        # Timer for general updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)  # ~60 FPS for smooth animations
        
        # Movement settings
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_pet)
        self.move_timer.start(50)
        
        self.speed = QPoint(2, 1)  # Slightly slower vertical movement
        self.direction = 1
        
        # Mood and state tracking
        self.happy = True
        self.talking = False
        self.talk_timer = QTimer()
        self.talk_timer.timeout.connect(self.stop_talking)
        
        # Shadow effect
        self.shadow_offset = QPoint(5, 5)
        
        # Colors
        self.body_color = QColor(245, 230, 210)  # Light cream color for cat
        self.head_color = QColor(245, 230, 210)  # Same as body
        self.accent_color = QColor(180, 160, 140)  # Darker accent for stripes
        self.pepper_color = QColor(40, 160, 40)  # Green for pepper
        self.pepper_stem_color = QColor(30, 120, 30)  # Darker green for stem
        
        # Size settings
        self.body_size = QSize(130, 120)
        self.head_size = QSize(90, 85)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # Save the current state
        painter.save()
        
        # Draw tail
        self.draw_tail(painter, center_x, center_y)
        
        # Draw shadow for body
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 40))
        shadow_rect = QRect(
            int(center_x - int(self.body_size.width() * self._body_scale) // 2 + self.shadow_offset.x()),
            int(center_y - int(self.body_size.height() * self._body_scale) // 2 + self.shadow_offset.y() + 30),
            int(self.body_size.width() * self._body_scale),
            int(self.body_size.height() * self._body_scale)
        )
        painter.drawEllipse(shadow_rect)
        
        # Create gradient for body
        body_gradient = QRadialGradient(
            center_x, center_y + 30, 
            self.body_size.width() // 2
        )
        body_gradient.setColorAt(0, self.body_color.lighter(110))
        body_gradient.setColorAt(0.7, self.body_color)
        body_gradient.setColorAt(1, self.body_color.darker(105))
        
        # Draw body
        painter.setPen(QPen(self.body_color.darker(120), 2))
        painter.setBrush(body_gradient)
        body_rect = QRect(
            int(center_x - int(self.body_size.width() * self._body_scale) // 2),
            int(center_y - int(self.body_size.height() * self._body_scale) // 2 + 30),
            int(self.body_size.width() * self._body_scale),
            int(self.body_size.height() * self._body_scale)
        )
        painter.drawEllipse(body_rect)
        
        # Draw cat stripes on body
        self.draw_cat_stripes(painter, center_x, center_y)
        
        # Draw belly
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 245, 235))  # Lighter color for belly
        belly_size = int(self.body_size.width() * 0.6 * self._body_scale)
        painter.drawEllipse(
            int(center_x - belly_size // 2),
            int(center_y - belly_size // 2 + 40),
            int(belly_size),
            int(belly_size)
        )
        
        # Draw shadow for head
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 40))
        shadow_head_rect = QRect(
            int(center_x - int(self.head_size.width() * self._body_scale) // 2 + self.shadow_offset.x()),
            int(center_y - int(self.head_size.height() * self._body_scale) // 2 - 30 + self.shadow_offset.y()),
            int(self.head_size.width() * self._body_scale),
            int(self.head_size.height() * self._body_scale)
        )
        painter.drawEllipse(shadow_head_rect)
        
        # Save state before head rotation
        painter.save()
        
        # Apply head rotation
        painter.translate(center_x, center_y - 30)
        painter.rotate(self._head_rotation)
        painter.translate(-center_x, -(center_y - 30))
        
        # Create gradient for head
        head_gradient = QRadialGradient(
            center_x, center_y - 30, 
            self.head_size.width() // 2
        )
        head_gradient.setColorAt(0, self.head_color.lighter(110))
        head_gradient.setColorAt(0.7, self.head_color)
        head_gradient.setColorAt(1, self.head_color.darker(105))
        
        # Draw head
        painter.setPen(QPen(self.head_color.darker(120), 2))
        painter.setBrush(head_gradient)
        head_rect = QRect(
            int(center_x - int(self.head_size.width() * self._body_scale) // 2),
            int(center_y - int(self.head_size.height() * self._body_scale) // 2 - 30),
            int(self.head_size.width() * self._body_scale),
            int(self.head_size.height() * self._body_scale)
        )
        painter.drawEllipse(head_rect)
        
        # Draw cat stripes on head
        self.draw_head_stripes(painter, center_x, center_y)
        
        # Draw ears
        self.draw_cat_ears(painter, center_x, center_y)
        
        # Draw green pepper hat
        self.draw_pepper_hat(painter, center_x, center_y)
        
        # Draw eyes
        self.draw_cat_eyes(painter, center_x, center_y)
        
        # Draw nose
        painter.setPen(QPen(QColor(255, 150, 150), 1))
        painter.setBrush(QBrush(QColor(255, 150, 150)))
        nose_size = 6
        painter.drawEllipse(
            int(center_x - nose_size // 2),
            int(center_y - 25),
            int(nose_size),
            int(nose_size)
        )
        
        # Draw mouth
        self.draw_cat_mouth(painter, center_x, center_y)
        
        # Draw whiskers
        self.draw_whiskers(painter, center_x, center_y)
        
        # Restore state after head rotation
        painter.restore()
        
        # Draw paws
        self.draw_paws(painter, center_x, center_y)
        
        # Restore the original state
        painter.restore()

    def draw_cat_ears(self, painter, center_x, center_y):
        # Draw triangular cat ears
        painter.setPen(QPen(self.head_color.darker(120), 2))
        
        # Left ear
        ear_path = QPainterPath()
        ear_path.moveTo(int(center_x - 35), int(center_y - 65))
        ear_path.lineTo(int(center_x - 50), int(center_y - 95))
        ear_path.lineTo(int(center_x - 20), int(center_y - 75))
        ear_path.closeSubpath()
        
        # Fill with gradient
        ear_gradient = QLinearGradient(
            int(center_x - 35), int(center_y - 95),
            int(center_x - 35), int(center_y - 65)
        )
        ear_gradient.setColorAt(0, self.head_color)
        ear_gradient.setColorAt(1, self.head_color.darker(110))
        
        painter.setBrush(ear_gradient)
        painter.drawPath(ear_path)
        
        # Inner ear detail
        inner_ear_path = QPainterPath()
        inner_ear_path.moveTo(int(center_x - 33), int(center_y - 70))
        inner_ear_path.lineTo(int(center_x - 43), int(center_y - 90))
        inner_ear_path.lineTo(int(center_x - 23), int(center_y - 75))
        inner_ear_path.closeSubpath()
        
        painter.setBrush(QColor(255, 200, 200))
        painter.drawPath(inner_ear_path)
        
        # Right ear
        ear_path = QPainterPath()
        ear_path.moveTo(int(center_x + 35), int(center_y - 65))
        ear_path.lineTo(int(center_x + 50), int(center_y - 95))
        ear_path.lineTo(int(center_x + 20), int(center_y - 75))
        ear_path.closeSubpath()
        
        # Fill with gradient
        ear_gradient = QLinearGradient(
            int(center_x + 35), int(center_y - 95),
            int(center_x + 35), int(center_y - 65)
        )
        ear_gradient.setColorAt(0, self.head_color)
        ear_gradient.setColorAt(1, self.head_color.darker(110))
        
        painter.setBrush(ear_gradient)
        painter.drawPath(ear_path)
        
        # Inner ear detail
        inner_ear_path = QPainterPath()
        inner_ear_path.moveTo(int(center_x + 33), int(center_y - 70))
        inner_ear_path.lineTo(int(center_x + 43), int(center_y - 90))
        inner_ear_path.lineTo(int(center_x + 23), int(center_y - 75))
        inner_ear_path.closeSubpath()
        
        painter.setBrush(QColor(255, 200, 200))
        painter.drawPath(inner_ear_path)

    def draw_pepper_hat(self, painter, center_x, center_y):
        # Save state for pepper rotation
        painter.save()
        
        # Apply slight rotation and bounce to pepper
        pepper_y_offset = -self._pepper_bounce
        painter.translate(center_x, center_y - 80 + pepper_y_offset)
        painter.rotate(self._head_rotation * 1.2)  # Slightly exaggerated rotation
        
        # Draw pepper stem
        stem_path = QPainterPath()
        stem_path.moveTo(0, -15)
        stem_path.cubicTo(-5, -25, 5, -25, 0, -35)
        
        painter.setPen(QPen(self.pepper_stem_color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawPath(stem_path)
        
        # Draw small leaf on stem
        leaf_path = QPainterPath()
        leaf_path.moveTo(-2, -25)
        leaf_path.cubicTo(-10, -30, -12, -20, -5, -18)
        leaf_path.closeSubpath()
        
        painter.setBrush(QColor(60, 180, 60))
        painter.setPen(QPen(QColor(40, 140, 40), 1))
        painter.drawPath(leaf_path)
        
        # Draw pepper body
        pepper_path = QPainterPath()
        pepper_path.moveTo(0, 0)
        pepper_path.cubicTo(-15, -5, -20, -30, 0, -15)  # Left side
        pepper_path.cubicTo(20, -30, 15, -5, 0, 0)      # Right side
        
        # Create gradient for pepper
        pepper_gradient = QLinearGradient(0, -15, 0, 0)
        pepper_gradient.setColorAt(0, self.pepper_color.lighter(120))
        pepper_gradient.setColorAt(0.5, self.pepper_color)
        pepper_gradient.setColorAt(1, self.pepper_color.darker(110))
        
        painter.setBrush(pepper_gradient)
        painter.setPen(QPen(self.pepper_color.darker(130), 2))
        painter.drawPath(pepper_path)
        
        # Draw pepper details/highlights
        highlight_path = QPainterPath()
        highlight_path.moveTo(-5, -10)
        highlight_path.cubicTo(-10, -15, -8, -25, -3, -15)
        
        painter.setPen(QPen(self.pepper_color.lighter(130), 1, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawPath(highlight_path)
        
        # Restore state
        painter.restore()

    def draw_cat_eyes(self, painter, center_x, center_y):
        # Draw cat eyes (almond shaped)
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        
        # Eye background (white part)
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        
        # Left eye
        eye_y_pos = center_y - 35
        left_eye_x = center_x - 20
        
        left_eye = QPainterPath()
        left_eye.addEllipse(
            int(left_eye_x - self._eye_size // 2 - 2),
            int(eye_y_pos - self._eye_size // 2),
            int(self._eye_size + 4),
            int(self._eye_size)
        )
        painter.drawPath(left_eye)
        
        # Right eye
        right_eye_x = center_x + 20
        
        right_eye = QPainterPath()
        right_eye.addEllipse(
            int(right_eye_x - self._eye_size // 2 - 2),
            int(eye_y_pos - self._eye_size // 2),
            int(self._eye_size + 4),
            int(self._eye_size)
        )
        painter.drawPath(right_eye)
        
        # Draw pupils (cat-like vertical slits)
        if self._eye_size > 5:  # Only draw pupils if eyes are open enough
            # Add slight movement to pupils based on mouse position
            cursor_pos = self.mapFromGlobal(QCursor.pos())
            dx = (cursor_pos.x() - center_x) / 100
            dy = (cursor_pos.y() - center_y) / 100
            
            # Limit pupil movement
            dx = max(min(dx, 2), -2)
            dy = max(min(dy, 2), -2)
            
            # Draw cat pupils (vertical ellipses)
            painter.setBrush(QBrush(QColor(0, 0, 0)))
            
            # Left pupil
            pupil_width = self._eye_size * 0.3
            pupil_height = self._eye_size * 0.8
            
            painter.drawEllipse(
                int(left_eye_x - pupil_width // 2 + dx),
                int(eye_y_pos - pupil_height // 2 + dy),
                int(pupil_width),
                int(pupil_height)
            )
            
            # Right pupil
            painter.drawEllipse(
                int(right_eye_x - pupil_width // 2 + dx),
                int(eye_y_pos - pupil_height // 2 + dy),
                int(pupil_width),
                int(pupil_height)
            )
            
            # Draw eye shine
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            shine_size = pupil_width * 0.8
            
            # Left eye shine
            painter.drawEllipse(
                int(left_eye_x - pupil_width // 4 + dx),
                int(eye_y_pos - pupil_height // 4 + dy),
                int(shine_size),
                int(shine_size)
            )
            
            # Right eye shine
            painter.drawEllipse(
                int(right_eye_x - pupil_width // 4 + dx),
                int(eye_y_pos - pupil_height // 4 + dy),
                int(shine_size),
                int(shine_size)
            )

    def draw_cat_mouth(self, painter, center_x, center_y):
        painter.setPen(QPen(QColor(0, 0, 0), 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        if self.talking:
            # Talking mouth (small oval)
            mouth_width = 16 + int(self._mouth_curve)
            mouth_height = 12 + int(self._mouth_curve / 2)
            painter.setBrush(QColor(255, 150, 150, 150))
            painter.drawEllipse(
                int(center_x - mouth_width // 2),
                int(center_y - 15),
                int(mouth_width),
                int(mouth_height)
            )
        else:
            # Cat mouth (small curved line)
            smile_width = 16
            smile_curve = int(self._mouth_curve / 2)
            
            # Draw the small curved line for mouth
            mouth_path = QPainterPath()
            mouth_path.moveTo(int(center_x - smile_width // 2), int(center_y - 15))
            mouth_path.quadTo(
                int(center_x), 
                int(center_y - 15 + smile_curve),
                int(center_x + smile_width // 2), 
                int(center_y - 15)
            )
            
            painter.setPen(QPen(QColor(100, 80, 80), 1.5))
            painter.drawPath(mouth_path)

    def draw_whiskers(self, painter, center_x, center_y):
        painter.setPen(QPen(QColor(200, 200, 200), 1.5))
        
        # Left whiskers
        painter.drawLine(int(center_x - 15), int(center_y - 20), int(center_x - 45), int(center_y - 25))
        painter.drawLine(int(center_x - 15), int(center_y - 15), int(center_x - 48), int(center_y - 15))
        painter.drawLine(int(center_x - 15), int(center_y - 10), int(center_x - 45), int(center_y - 5))
        
        # Right whiskers
        painter.drawLine(int(center_x + 15), int(center_y - 20), int(center_x + 45), int(center_y - 25))
        painter.drawLine(int(center_x + 15), int(center_y - 15), int(center_x + 48), int(center_y - 15))
        painter.drawLine(int(center_x + 15), int(center_y - 10), int(center_x + 45), int(center_y - 5))

    def draw_paws(self, painter, center_x, center_y):
        paw_color = self.body_color.lighter(105)
        painter.setPen(QPen(paw_color.darker(120), 2))
        painter.setBrush(paw_color)
        
        # Front paws
        # Left paw
        painter.drawEllipse(
            int(center_x - 50),
            int(center_y + 60),
            30,
            20
        )
        
        # Right paw
        painter.drawEllipse(
            int(center_x + 20),
            int(center_y + 60),
            30,
            20
        )
        
        # Paw details (toe beans)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 200, 200))
        
        # Left paw beans
        for i in range(3):
            painter.drawEllipse(
                int(center_x - 50 + i * 8),
                int(center_y + 60 - 5),
                6,
                6
            )
        
        # Right paw beans
        for i in range(3):
            painter.drawEllipse(
                int(center_x + 20 + i * 8),
                int(center_y + 60 - 5),
                6,
                6
            )

    def draw_tail(self, painter, center_x, center_y):
        # Draw cat tail (curved)
        tail_path = QPainterPath()
        
        # Start point at the back of the body
        tail_start_x = center_x - 10
        tail_start_y = center_y + 40
        
        # Apply tail animation
        tail_angle_rad = math.radians(self._tail_angle)
        tail_curve_x = -40 * math.cos(tail_angle_rad)
        tail_curve_y = 20 * math.sin(tail_angle_rad)
        
        tail_path.moveTo(tail_start_x, tail_start_y)
        tail_path.cubicTo(
            int(tail_start_x - 30), int(tail_start_y + 10),
            int(tail_start_x - 60), int(tail_start_y + tail_curve_y),
            int(tail_start_x - 80 + tail_curve_x), int(tail_start_y - 20 + tail_curve_y)
        )
        
        # Draw tail shadow
        shadow_path = QPainterPath()
        shadow_path.moveTo(tail_start_x + 2, tail_start_y + 2)
        shadow_path.cubicTo(
            int(tail_start_x - 30 + 2), int(tail_start_y + 10 + 2),
            int(tail_start_x - 60 + 2), int(tail_start_y + tail_curve_y + 2),
            int(tail_start_x - 80 + tail_curve_x + 2), int(tail_start_y - 20 + tail_curve_y + 2)
        )
        
        painter.setPen(QPen(QColor(0, 0, 0, 40), 12, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawPath(shadow_path)
        
        # Create gradient for tail
        tail_gradient = QLinearGradient(
            tail_start_x, tail_start_y,
            int(tail_start_x - 80 + tail_curve_x), int(tail_start_y - 20 + tail_curve_y)
        )
        tail_gradient.setColorAt(0, self.body_color)
        tail_gradient.setColorAt(1, self.body_color.darker(110))
        
        painter.setPen(QPen(tail_gradient, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawPath(tail_path)
        
        # Draw tail stripes
        stripe_color = self.accent_color
        painter.setPen(QPen(stripe_color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        
        # Calculate points along the tail for stripes
        for i in range(1, 4):
            t = i / 4.0
            stripe_x = int(tail_start_x - (80 - tail_curve_x) * t)
            stripe_y = int(tail_start_y + (10 + tail_curve_y) * t - 20 * t * t)
            
            # Draw a small line perpendicular to the tail direction
            angle = math.atan2(
                (tail_start_y - 20 + tail_curve_y) - tail_start_y,
                (tail_start_x - 80 + tail_curve_x) - tail_start_x
            ) + math.pi/2
            
            stripe_length = 8
            painter.drawLine(
                int(stripe_x - stripe_length * math.cos(angle)),
                int(stripe_y - stripe_length * math.sin(angle)),
                int(stripe_x + stripe_length * math.cos(angle)),
                int(stripe_y + stripe_length * math.sin(angle))
            )

    def draw_cat_stripes(self, painter, center_x, center_y):
        # Draw tabby cat stripes on body
        stripe_color = self.accent_color
        painter.setPen(QPen(stripe_color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        
        # Back stripes
        for i in range(3):
            y_offset = i * 15
            stripe_path = QPainterPath()
            stripe_path.moveTo(int(center_x - 40), int(center_y + 10 + y_offset))
            stripe_path.cubicTo(
                int(center_x - 30), int(center_y + 5 + y_offset),
                int(center_x - 20), int(center_y + 15 + y_offset),
                int(center_x - 10), int(center_y + 10 + y_offset)
            )
            painter.drawPath(stripe_path)
        
        # Side stripes
        for i in range(2):
            y_offset = i * 15
            stripe_path = QPainterPath()
            stripe_path.moveTo(int(center_x + 30), int(center_y + 20 + y_offset))
            stripe_path.cubicTo(
                int(center_x + 20), int(center_y + 15 + y_offset),
                int(center_x + 10), int(center_y + 25 + y_offset),
                int(center_x), int(center_y + 20 + y_offset)
            )
            painter.drawPath(stripe_path)

    def draw_head_stripes(self, painter, center_x, center_y):
        # Draw tabby cat stripes on head
        stripe_color = self.accent_color
        painter.setPen(QPen(stripe_color, 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        
        # Forehead marking (M shape typical for tabbies)
        m_path = QPainterPath()
        m_path.moveTo(int(center_x - 20), int(center_y - 55))
        m_path.lineTo(int(center_x - 10), int(center_y - 45))
        m_path.lineTo(int(center_x), int(center_y - 55))
        m_path.lineTo(int(center_x + 10), int(center_y - 45))
        m_path.lineTo(int(center_x + 20), int(center_y - 55))
        
        painter.drawPath(m_path)
        
        # Cheek markings
        painter.drawLine(
            int(center_x - 30), int(center_y - 25),
            int(center_x - 20), int(center_y - 15)
        )
        
        painter.drawLine(
            int(center_x + 30), int(center_y - 25),
            int(center_x + 20), int(center_y - 15)
        )

    def update_pet(self):
        self.update()  # Redraw the interface

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Show input dialog
            dialog = ModernInputDialog(self)
            if dialog.exec():
                prompt = dialog.prompt_input.text()
                if prompt.lower() in ["exit", "quit"]:
                    logger.info("Goodbye!")
                    QApplication.quit()
                elif not prompt.strip():
                    logger.warning("Skipping empty prompt.")
                else:
                    logger.warning("Processing your request...")
                    # Start talking animation
                    self.start_talking()
                    # Call the main function
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    loop.run_until_complete(self.main(prompt))

    def start_talking(self):
        self.talking = True
        # Stop talking after 5 seconds
        self.talk_timer.start(5000)
        
    def stop_talking(self):
        self.talking = False
        self.talk_timer.stop()

    async def main(self, prompt):
        # This is your main function logic
        agent = Manus()
        await agent.run(prompt)
        # Stop talking when processing is done
        self.stop_talking()

    def move_pet(self):
        # Get current window position
        current_pos = self.pos()
        
        # Update position
        new_pos = current_pos + self.speed
        
        # Check if hitting screen edges
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        
        if new_pos.x() < 0 or new_pos.x() + self.width() > screen_geometry.width():
            self.speed.setX(-self.speed.x())  # Reverse horizontal direction
        if new_pos.y() < 0 or new_pos.y() + self.height() > screen_geometry.height():
            self.speed.setY(-self.speed.y())  # Reverse vertical direction
        
        # Set new position
        self.move(new_pos)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Use globalPosition() instead of globalPos()
            global_position = event.globalPosition().toPoint()
            self.drag_position = global_position - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
            global_position = event.globalPosition().toPoint()
            self.move(global_position - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show the pet
    pet = DesktopPet()
    pet.show()
    
    sys.exit(app.exec())