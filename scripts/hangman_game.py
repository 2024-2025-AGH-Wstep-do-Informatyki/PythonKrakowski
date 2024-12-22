import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt

class HangmanGame(QWidget):
    def __init__(self, hub_window):
        super().__init__()
        
        self.hub_window = hub_window
        self.setWindowTitle("Wisielec")
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon(r".\assets\icon_pic.jpg"))

        with open(r".\assets\hangman\wisielec_slowa.txt", "r", encoding="utf-8") as file:
            self.word_list = [line.strip() for line in file]
        
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(270, 380)
        self.image_label.move(15, 0) 
        
        buttons_container = QWidget(self)
        buttons_container.setFixedSize(200, 350)
        buttons_container.move(285, 5)
        
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.buttons = {}
        row, x, y = 1, 10, 10  
        for index, letter in enumerate(alphabet):
            button = QPushButton(letter, buttons_container)
            button.setFont(QFont("Arial", 12))
            button.setFixedSize(60, 35)
            button.clicked.connect(lambda checked, l=letter: self.handle_guess(l))
            button.move(x, y)
            self.buttons[letter] = button
            x += 65
            if (index + 1) % 3 == 0:
                row += 1
                x = 10
                y += 35
                if(row > 8):
                    x += 30

        self.lives_label = QLabel(self)
        self.lives_label.setFont(QFont("Arial", 10))
        self.lives_label.setAlignment(Qt.AlignCenter)
        self.lives_label.setFixedWidth(self.width())
        self.lives_label.move(0, 450)

        self.word_label = QLabel(self)
        self.word_label.setStyleSheet("font-size: 33px")
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setFixedWidth(self.width())
        self.word_label.move(0, 380)
        
        self.start_game()

        
    def start_game(self):
        self.word_to_guess = random.choice(self.word_list)
        self.guessed_word = ["_"] * len(self.word_to_guess)
        self.lives = 8
        self.update_hangman_image()
        self.lives_label.setText(f"Pozostałych żyć: {self.lives}")
        self.word_label.setStyleSheet("color: black; font-size: 33px")
        self.word_label.setText(" ".join(self.guessed_word))

        for button in self.buttons.values():
            button.setEnabled(True)
    
    def handle_guess(self, letter):
        button = self.buttons[letter]
        button.setEnabled(False) #każdy przycisk po kliknięciu automatycznie zostaje "wyłączony"

        if letter in self.word_to_guess: #jeżeli wybrana litera jest w słowie do odgadnięcia, program wyswietli ja w odpowiednim miejscu
            for i, l in enumerate(self.word_to_guess):
                if l == letter:
                    self.guessed_word[i] = letter
            self.word_label.setText(" ".join(self.guessed_word))

        else: #jezeli litery nie bylo w szukanym slowie gracz traci zycie i zmienia sie obrazek
            self.lives -= 1
            self.lives_label.setText(f"Pozostałych żyć: {self.lives}")
            self.update_hangman_image()
        self.end_game_check()

    def update_hangman_image(self):
        image= f"./assets/hangman/wisielec{8-self.lives}.jpg" 
        pixmap = QPixmap(image)
        scaled_pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(scaled_pixmap)

    def end_game_check(self):
        if self.lives <= 0: #jezeli gracz straci wszystkie zycia to przegrywa
                self.word_label.setStyleSheet("color:red; font-size: 30px")
                self.word_label.setText(f"Przegrałeś. Słowo to {self.word_to_guess}")
                for button in self.buttons.values():
                    button.setEnabled(False)
                self.ask_restart()
        elif "_" not in self.guessed_word: #jezeli całe slowo jest odgadniete gracz wygrywa
                self.word_label.setStyleSheet("color:red; font-size: 30px")
                self.word_label.setText(f"Odgadłeś słowo {self.word_to_guess}")
                for button in self.buttons.values():
                    button.setEnabled(False)
                self.ask_restart()

    def ask_restart(self):
        msg = QMessageBox()
        msg.setWindowIcon(QIcon("./assets/icon_pic.jpg"))
        #msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Koniec gry")
        msg.setText("Czy chcesz zagrać ponownie?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        if msg.exec_() == QMessageBox.Yes:
            self.start_game()
        else:
            self.close()
            self.hub_window.show()
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HangmanGame(None)
    window.show()
    sys.exit(app.exec_())

