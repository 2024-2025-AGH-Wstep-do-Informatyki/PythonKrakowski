import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont, QIcon
from PyQt5.QtCore import QTimer, Qt, QRect
import random

class DinoGame(QMainWindow):
    def __init__(self, hub_window):
        super().__init__()

        self.hub_window = hub_window

        self.setWindowTitle("Dino Game")
        self.setFixedSize(1000, 370)
        self.setWindowIcon(QIcon("./assets/icon_pic.jpg"))

        self.dino_x = 50
        self.dino_y = 300
        self.dino_width = 30
        self.dino_height = 30
        self.is_jumping = False
        self.jump_strength = 15
        self.jump_count = self.jump_strength
        self.gravity = 2.5

        self.ground_y = 300

        self.obstacles = []
        self.cactus_speed = 7

        self.score = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(30)

        self.score_timer = QTimer()
        self.score_timer.timeout.connect(self.add_points)
        self.score_timer.start(100)

        self.difficulty_timer = QTimer()
        self.difficulty_timer.timeout.connect(self.increase_difficulty)
        self.difficulty_timer.start(5000)

        self.obstacle_timer = QTimer()
        self.obstacle_timer.timeout.connect(self.generate_obstacle)
        self.obstacle_timer.start(self.get_obstacle_interval())

    def update_game(self):
        for obstacle in self.obstacles:
            obstacle['x'] -= self.cactus_speed
            if obstacle['x'] < 0:
                self.obstacles.remove(obstacle)

        if self.is_jumping:
            if self.jump_count >= -self.jump_strength:
                direction = 1 if self.jump_count > 0 else -1
                self.dino_y -= direction * (self.jump_count ** 2) * 0.1
                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = self.jump_strength
        else:
            if self.dino_y + self.dino_height < self.ground_y:
                self.dino_y += self.gravity

            if self.dino_y + self.dino_height > self.ground_y:
                self.dino_y = self.ground_y - self.dino_height

        for obstacle in self.obstacles:
            if self.check_collision(self.dino_x, self.dino_y, self.dino_width, self.dino_height,
                                    obstacle['x'], self.ground_y - obstacle['height'], obstacle['width'], obstacle['height']):
                self.game_over()

        self.update()

    def add_points(self):
        self.score += 1

    def increase_difficulty(self):
        self.cactus_speed += 1
        self.adjust_obstacle_interval()

    def check_collision(self, x1, y1, w1, h1, x2, y2, w2, h2):
        return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Space and not self.is_jumping:
            self.is_jumping = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        painter.drawRect(QRect(int(self.dino_x), int(self.dino_y), int(self.dino_width), int(self.dino_height)))

        for obstacle in self.obstacles:
            painter.setBrush(QBrush(QColor(255, 0, 0)))
            painter.drawRect(QRect(int(obstacle['x']), int(self.ground_y - obstacle['height']),
                                   int(obstacle['width']), int(obstacle['height'])))

        painter.setBrush(QBrush(QColor(100, 100, 100)))
        painter.drawRect(0, self.ground_y, self.width(), 70)

        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont('Arial', 16))
        painter.drawText(self.width() // 2 - 50, 30, f"Score: {self.score}")

    def generate_obstacle(self):
        width = random.randint(20, 50)
        height = random.randint(50, 100)
        x_position = self.width()
        self.obstacles.append({'x': x_position, 'width': width, 'height': height})

        self.adjust_obstacle_interval()

    def adjust_obstacle_interval(self):
        new_interval = max(1000, 3000 - self.cactus_speed * 100)
        self.obstacle_timer.start(new_interval)

    def get_obstacle_interval(self):
        return 1500

    def game_over(self):
        self.timer.stop()
        self.score_timer.stop()
        self.difficulty_timer.stop()
        self.obstacle_timer.stop()
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(f"Koniec gry! Wynik: {self.score}")
        msg_box.setInformativeText("Czy chcesz zagrać ponownie?")
        
        yes_button = msg_box.addButton("Tak", QMessageBox.YesRole)
        no_button = msg_box.addButton("Nie", QMessageBox.NoRole)
        
        msg_box.exec_()
        
        if msg_box.clickedButton() == yes_button:
            self.reset_game()
        elif msg_box.clickedButton() == no_button:
            self.close()
            self.hub_window.show()

    def reset_game(self):
        self.dino_x = 50
        self.dino_y = 300
        self.score = 0
        self.cactus_speed = 7
        self.obstacles.clear()
        self.timer.start(30)
        self.score_timer.start(100)
        self.difficulty_timer.start(5000)
        self.obstacle_timer.start(self.get_obstacle_interval())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = DinoGame(None)
    game.show()
    sys.exit(app.exec_())
