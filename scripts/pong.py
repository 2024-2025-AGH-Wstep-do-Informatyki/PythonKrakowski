import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QDesktopWidget
from PyQt5.QtGui import QPainter, QColor, QFont, QKeyEvent, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRect

class PongGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("PONG")
        self.setFixedSize(800, 600)
        self.center()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.canvas = Canvas()
        self.layout.addWidget(self.canvas)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def keyPressEvent(self, event: QKeyEvent):
        self.canvas.keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        self.canvas.keyReleaseEvent(event)

    def update(self):
        self.canvas.update()

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        self.initGame()
        self.score1 = 0
        self.score2 = 0
        self.ball_image = QPixmap("./assets/icon_pic.jpg")

    def initGame(self):
        self.ball_x = 380
        self.ball_y = 280
        self.ball_dx = 5
        self.ball_dy = 5
        self.paddle1_x = 50
        self.paddle1_y = 250
        self.paddle2_x = 693
        self.paddle2_y = 250
        self.paddle_width = 30
        self.paddle_height = 100
        self.paddle_speed = 20
        self.keys = set()
        self.game_started = False
        self.countdown = 3

        self.start_timer = QTimer(self)
        self.start_timer.timeout.connect(self.updateCountdown)
        self.start_timer.start(1000)

    def startGame(self):
        self.game_started = True

    def updateCountdown(self):
        self.countdown -= 1
        if self.countdown <= 0:
            self.start_timer.stop()
            self.startGame()

    def keyPressEvent(self, event: QKeyEvent):
        self.keys.add(event.key())

    def keyReleaseEvent(self, event: QKeyEvent):
        self.keys.discard(event.key())

    def movePaddles(self):
        if Qt.Key_W in self.keys and self.paddle1_y > 0:
            self.paddle1_y -= self.paddle_speed
        if Qt.Key_S in self.keys and self.paddle1_y < 600 - self.paddle_height:
            self.paddle1_y += self.paddle_speed
        if Qt.Key_Up in self.keys and self.paddle2_y > 0:
            self.paddle2_y -= self.paddle_speed
        if Qt.Key_Down in self.keys and self.paddle2_y < 600 - self.paddle_height:
            self.paddle2_y += self.paddle_speed

    def moveBall(self):
        if self.game_started:
            self.ball_x += self.ball_dx
            self.ball_y += self.ball_dy

            if self.ball_y <= 0 or self.ball_y >= 580:
                self.ball_dy = -self.ball_dy

            if self.ball_x <= self.paddle1_x + self.paddle_width and self.paddle1_y < self.ball_y < self.paddle1_y + self.paddle_height:
                self.ball_dx = -self.ball_dx
            if self.ball_x >= self.paddle2_x and self.paddle2_y < self.ball_y < self.paddle2_y + self.paddle_height:
                self.ball_dx = -self.ball_dx

            if self.ball_x < 0:
                self.score2 += 1
                self.initBallPosition()
            if self.ball_x > 800:
                self.score1 += 1
                self.initBallPosition()

    def initBallPosition(self):
        self.ball_x = 380
        self.ball_y = 280
        self.ball_dx = 5
        self.ball_dy = 5

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawGame(qp)
        qp.end()

    def drawGame(self, qp):
        qp.setBrush(QColor(101, 67, 33))
        qp.drawRect(self.rect())

        qp.drawPixmap(self.ball_x, self.ball_y, 40, 40, self.ball_image)

        qp.setPen(QColor(0, 0, 0))
        qp.setBrush(QColor(0, 255, 0))
        qp.drawRect(self.paddle1_x, self.paddle1_y, self.paddle_width, self.paddle_height)
        qp.setBrush(QColor(255, 69, 0))
        qp.drawRect(self.paddle2_x, self.paddle2_y, self.paddle_width, self.paddle_height)

        text = f"Wynik: {self.score1} - {self.score2}"
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont("Arial", 20))
        qp.drawText(self.rect(), Qt.AlignTop | Qt.AlignHCenter, text)

        if not self.game_started:
            countdown_text = f"Start za: {self.countdown}"
            qp.setPen(QColor(255, 255, 0))
            qp.setFont(QFont("Arial", 40, QFont.Bold))
            qp.drawText(self.rect(), Qt.AlignCenter, countdown_text)

    def update(self):
        self.movePaddles()
        self.moveBall()
        self.repaint()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = PongGame()
    game.show()
    sys.exit(app.exec_())