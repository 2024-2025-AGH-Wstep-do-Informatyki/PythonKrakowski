from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QIcon
import sys
from scripts.snake import SnakeGame
from scripts.dino import DinoGame
from scripts.tictactoe_game import TicTacToe
from scripts.saper import SaperGame
from scripts.hangman_game import HangmanGame

class GameHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Hub")
        self.setWindowIcon(QIcon("./assets/icon_pic.jpg"))

        layout = QVBoxLayout()
        self.btn_snake = QPushButton("Snake Game")
        self.btn_snake.setFixedSize(250,40)
        self.btn_dino = QPushButton("Dino Game")
        self.btn_dino.setFixedSize(250,40)
        self.btn_ttt = QPushButton("Tic-Tac-Toe Game")
        self.btn_ttt.setFixedSize(250,40)
        self.btn_saper = QPushButton("Saper Game")
        self.btn_saper.setFixedSize(250,40)
        self.btn_hangman = QPushButton("Hangman Game")
        self.btn_hangman.setFixedSize(250,40)

        self.btn_snake.clicked.connect(self.open_snake_game)
        self.btn_dino.clicked.connect(self.open_dino_game)
        self.btn_ttt.clicked.connect(self.open_tictactoe_game)
        self.btn_saper.clicked.connect(self.open_saper_game)
        self.btn_hangman.clicked.connect(self.open_hangman_game)

        layout.addWidget(self.btn_snake)
        layout.addWidget(self.btn_dino)
        layout.addWidget(self.btn_ttt)
        layout.addWidget(self.btn_saper)
        layout.addWidget(self.btn_hangman)

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

    def open_saper_game(self):
        self.Saper = SaperGame(self)
        self.Saper.show()
        self.hide()

    def open_hangman_game(self):
        self.Hangman = HangmanGame(self)
        self.Hangman.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameHub()
    window.show()
    sys.exit(app.exec_())
