import sys
import random
import math
from PyQt5.QtCore import Qt, QTimer, QPointF, QPropertyAnimation, QRect
from PyQt5.QtGui import QPainter, QColor, QPen, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox

class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        self.exploded = False

    def update(self):
        if not self.exploded:
            self.explode()
        for particle in self.particles:
            particle.update()

    def explode(self):
        self.exploded = True
        num_particles = random.randint(400, 500)  
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(15, 25) 
            life = random.randint(50, 150)
            self.particles.append(Particle(self.x, self.y, angle, speed, life))

class Particle:
    def __init__(self, x, y, angle, speed, life):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.life = life
        self.alpha = 255
        #neonowe kolory: różowy, zielony, niebieski, żółty, fioletowy, pomarańczowy
        self.color = QColor(
            random.choice([255, 255, 0, 255, 255, 0, 255]),  
            random.choice([255, 0, 255, 255, 255, 0, 255]),
            random.choice([255, 0, 255, 255, 255, 255])     
        )
        self.size = random.randint(10, 25) 
        self.trail_length = random.randint(40, 80) 

    def update(self):
        if self.life > 0:
            self.x += self.speed * 0.3 * math.cos(self.angle)
            self.y += self.speed * 0.3 * math.sin(self.angle)
            self.life -= 1
            self.alpha = max(0, self.alpha - 8)
            self.color.setAlpha(self.alpha)

    def get_particle_positions(self):
        start_x = self.x - self.trail_length * math.cos(self.angle)
        start_y = self.y - self.trail_length * math.sin(self.angle)
        return QPointF(start_x, start_y), QPointF(self.x, self.y)

class FireworkWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Neonowe Fajerwerki!")
        self.setGeometry(100, 100, 800, 600)
        self.fireworks = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_fireworks)
        self.timer.start(30) 

        #uruchamianie wielu fajerwerków automatycznie co 300ms
        self.auto_firework_timer = QTimer(self)
        self.auto_firework_timer.timeout.connect(self.launch_firework)
        self.auto_firework_timer.start(300)

        #timer do wyświetlania komunikatu "You Won!" (po 1 sekundzie)
        self.display_message = False
        self.message_timer = QTimer(self)
        self.message_timer.timeout.connect(self.show_message)
        self.message_timer.start(1000)

        #ustawienia animacji dla komunikatu "You Won!!"
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(1000)
        self.animation.setLoopCount(-1)
        self.animation.setKeyValueAt(0, QPointF(400, 300))
        #self.animation.setKeyValueAt(0.5, QPointF(400, 270))  
        #self.animation.setKeyValueAt(1, QPointF(400, 300))    

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.black)
        painter.drawRect(0, 0, self.width(), self.height())

        for firework in self.fireworks:
            for particle in firework.particles:
                start_pos, end_pos = particle.get_particle_positions()
                pen = QPen(particle.color)
                pen.setWidth(random.randint(3, 6)) 
                painter.setPen(pen)
                painter.drawLine(start_pos, end_pos)

        if self.display_message:
            self.display_win_message(painter)

    def launch_firework(self):
        x = random.randint(100, self.width() - 100)
        y = random.randint(100, self.height() - 100)
        self.fireworks.append(Firework(x, y))

    def update_fireworks(self):
        for firework in self.fireworks[:]:
            firework.update()
            if all(particle.life <= 0 for particle in firework.particles):
                self.fireworks.remove(firework)
        self.update()

    def show_message(self):
        self.display_message = True
        self.message_timer.stop()

    def display_win_message(self, painter):
        painter.setPen(QPen(Qt.white))
        painter.setFont(QFont('Comic Sans MS', 48, QFont.Bold))
        text = "You Won!!"
        painter.setPen(QPen(QColor(255, 0, 0)))
        painter.drawText(QRect(200, 250, 400, 100), Qt.AlignCenter, text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FireworkWindow()
    window.show()
    sys.exit(app.exec_())
