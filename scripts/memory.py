import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QPushButton, QMessageBox, QWidget, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

GRID_SIZE = 4
CARD_IMAGES = ["🐍", "🦑", "🦎", "🦜", "🦋", "🐢", "🐉", "🐊"]
NUM_PAIRS = len(CARD_IMAGES)
CARD_BACK = "🔒"

class MemoryGame(QMainWindow):
    def __init__(self, hub_window):
        super().__init__()
        self.hub_window = hub_window
        self.setWindowTitle("Gra Memory")
        self.setStyleSheet("background-color: #2E8B57;")
        self.grid = []
        self.first_card = None
        self.second_card = None
        self.matches_found = 0
        self.attempts = 0
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.cards = {}
        card_values = random.sample(CARD_IMAGES * 2, len(CARD_IMAGES) * 2)

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                card_value = card_values.pop()
                button = QPushButton(CARD_BACK)
                button.setFixedSize(150, 150)
                font = QFont()
                font.setPointSize(32)
                button.setFont(font)
                button.setStyleSheet("""
                    background-color: #6B8E23;
                    color: white;
                    border-radius: 10px;
                    font-weight: bold;
                    border: 2px solid #556B2F;
                """)
                button.clicked.connect(self.card_click)
                self.cards[(i, j)] = {"button": button, "value": card_value, "revealed": False}
                self.layout.addWidget(button, i, j)

        self.attempts_label = QLabel(f'Próby: {self.attempts}', self)
        self.attempts_label.setStyleSheet("color: white;")
        font = QFont()
        font.setPointSize(48)
        self.attempts_label.setFont(font)
        self.layout.addWidget(self.attempts_label, GRID_SIZE, 0, 1, GRID_SIZE, Qt.AlignCenter)

    def card_click(self):
        if self.first_card is not None and self.second_card is not None:
            return

        button = self.sender()
        position = next((pos for pos, card in self.cards.items() if card["button"] == button), None)
        if position is None:
            return

        card = self.cards[position]
        if card["revealed"]:
            return

        card["button"].setText(card["value"])
        card["revealed"] = True

        if self.first_card is None:
            self.first_card = position
        elif self.second_card is None:
            self.second_card = position
            self.attempts += 1
            self.attempts_label.setText(f'Próby: {self.attempts}')
            self.check_match()

    def check_match(self):
        first_card = self.cards[self.first_card]
        second_card = self.cards[self.second_card]

        self.set_buttons_enabled(False)

        if first_card["value"] == second_card["value"]:
            self.matches_found += 1
            if self.matches_found == NUM_PAIRS:
                self.game_won()
            QTimer.singleShot(500, self.reset_cards)
        else:
            QTimer.singleShot(1000, self.hide_cards)

    def reset_cards(self):
        self.first_card = None
        self.second_card = None
        self.set_buttons_enabled(True)

    def hide_cards(self):
        self.cards[self.first_card]["button"].setText(CARD_BACK)
        self.cards[self.second_card]["button"].setText(CARD_BACK)
        self.cards[self.first_card]["revealed"] = False
        self.cards[self.second_card]["revealed"] = False
        self.first_card = None
        self.second_card = None
        self.set_buttons_enabled(True)

    def set_buttons_enabled(self, enabled):
        for card in self.cards.values():
            card["button"].setEnabled(enabled)

    def game_won(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Gratulacje!")
        msg.setText(f"Wygrałeś! Znaleziono wszystkie pary w {self.attempts} próbach.")
        reply = QMessageBox.question(self, 'Kontynuować grę?', 'Czy chcesz zagrać ponownie?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            self.reset_game()
        else:
            self.close()
            self.hub_window.show()

    def reset_game(self):
        self.matches_found = 0
        self.attempts = 0
        self.attempts_label.setText(f'Próby: {self.attempts}')
        for card in self.cards.values():
            card["button"].setText(CARD_BACK)
            card["revealed"] = False
        card_values = random.sample(CARD_IMAGES * 2, len(CARD_IMAGES) * 2)
        for position, card in self.cards.items():
            card["value"] = card_values.pop()
        self.first_card = None
        self.second_card = None
        self.set_buttons_enabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = MemoryGame(None)
    game.show()
    sys.exit(app.exec_())
