import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPainter, QBrush, QColor
from PyQt5.QtCore import Qt, QTimer

class SnakeGame(QMainWindow):
    def __init__(self, hub_window):
        super().__init__()
        
        self.hub_window = hub_window

        self.init_game()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game)
        self.timer.start(100)

        self.initUI()

    def init_game(self):
        """Initialize or reset the game state."""
        self.snake = [(100, 100), (90, 100), (80, 100)]
        self.direction = 'RIGHT'
        self.place_food()

    def initUI(self):
        self.setFixedSize(400, 400)
        self.setWindowTitle('Snake Game')
        self.setFocusPolicy(Qt.StrongFocus)

    def place_food(self):
        x = random.randint(0, 39) * 10
        y = random.randint(0, 39) * 10
        self.food = (x, y)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(QColor(0, 255, 0)))
        for segment in self.snake:
            painter.drawRect(segment[0], segment[1], 10, 10)

        painter.setBrush(QBrush(QColor(255, 0, 0)))
        painter.drawRect(self.food[0], self.food[1], 10, 10)

    def update_game(self):
        head_x, head_y = self.snake[0]

        if self.direction == 'UP':
            head_y -= 10
        elif self.direction == 'DOWN':
            head_y += 10
        elif self.direction == 'LEFT':
            head_x -= 10
        elif self.direction == 'RIGHT':
            head_x += 10

        new_head = (head_x, head_y)

        if (new_head in self.snake or
                head_x < 0 or head_x >= 400 or
                head_y < 0 or head_y >= 400):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.place_food()
        else:
            self.snake.pop()

        self.update()

    def game_over(self):
        self.timer.stop()
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('Game Over')
        msg_box.setText('Koniec gry! Czy chcesz zagrać ponownie?')
        
        yes_button = msg_box.addButton('Tak', QMessageBox.YesRole)
        no_button = msg_box.addButton('Nie', QMessageBox.NoRole)
        
        msg_box.exec_()
        
        if msg_box.clickedButton() == yes_button:
            self.init_game()
            self.timer.start(100)
            self.update()
        elif msg_box.clickedButton() == no_button:
            self.close()
            self.hub_window.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up and self.direction != 'DOWN':
            self.direction = 'UP'
        elif event.key() == Qt.Key_Down and self.direction != 'UP':
            self.direction = 'DOWN'
        elif event.key() == Qt.Key_Left and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        elif event.key() == Qt.Key_Right and self.direction != 'LEFT':
            self.direction = 'RIGHT'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SnakeGame(None)
    game.show()
    sys.exit(app.exec_())