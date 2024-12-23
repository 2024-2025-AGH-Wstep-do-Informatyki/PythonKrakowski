from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import sys
from scripts.snake import SnakeGame
from scripts.dino import DinoGame
from scripts.tictactoe_game import TicTacToe
from scripts.saper import SaperGame
from scripts.hangman_game import HangmanGame
from scripts.game2048 import Game2048
from scripts.memory import MemoryGame
from scripts.sudoku import SudokuGame
from scripts.pong import PongGame

class GameHub(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GameHub")
        self.setWindowIcon(QIcon("./assets/icon_pic.jpg"))
        
        self.setStyleSheet("background-color: black;") 

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignCenter)  

        logo_label = QLabel(self)
        logo_pixmap = QPixmap("./assets/PyHub.png")
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(logo_label)

        main_layout.addSpacerItem(QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.games = [
            ("Snake Game", SnakeGame),
            ("Dino Game", DinoGame),
            ("Tic-Tac-Toe Game", TicTacToe),
            ("Saper Game", SaperGame),
            ("Hangman Game", HangmanGame),
            ("Memory Game", MemoryGame),
            ("2048 Game", Game2048),
            ("Sudoku Game", SudokuGame),
            ("Pong Game", PongGame),
        ]

        for game_name, game_class in self.games:
            game_button_layout = QHBoxLayout()
            game_button_layout.setAlignment(Qt.AlignCenter) 
            button = self.create_game_button(game_name, game_class)
            game_button_layout.addWidget(button)
            main_layout.addLayout(game_button_layout)

        main_layout.addSpacerItem(QSpacerItem(0, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_game_button(self, game_name, game_class):
        button = QPushButton(game_name)
        button.setFixedSize(250, 40)
        button.setStyleSheet( 
            """
            QPushButton {
                background-color: #333;
                color: white;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            """
        )
        button.clicked.connect(lambda: self.open_game(game_class))
        return button

    def open_game(self, game_class):
        self.current_game = game_class(self)
        self.current_game.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameHub()
    window.show()
    sys.exit(app.exec_())
