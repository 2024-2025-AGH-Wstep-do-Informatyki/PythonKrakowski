from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QIcon
import sys
from snake import SnakeGame
from dino import DinoGame
from tictactoe_game import TicTacToe

class GameHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Hub")
        self.setWindowIcon(QIcon('waz.jpg'))

        layout = QVBoxLayout()
        self.btn_snake = QPushButton("Snake Game")
        self.btn_dino = QPushButton("Dino Game")
        self.btn_ttt = QPushButton("Tic-Tac-Toe Game")

        self.btn_snake.clicked.connect(self.open_snake_game)
        self.btn_dino.clicked.connect(self.open_dino_game)
        self.btn_ttt.clicked.connect(self.open_tictactoe_game)

        layout.addWidget(self.btn_snake)
        layout.addWidget(self.btn_dino)
        layout.addWidget(self.btn_ttt)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_snake_game(self):
        self.snake_game = SnakeGame(self)
        self.snake_game.show()
        self.hide()

    def open_dino_game(self):
        self.dino_game = DinoGame(self)
        self.dino_game.show()
        self.hide()

    def open_tictactoe_game(self):
        self.TicTacToe = TicTacToe(self)
        self.TicTacToe.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameHub()
    window.show()
    sys.exit(app.exec_())
