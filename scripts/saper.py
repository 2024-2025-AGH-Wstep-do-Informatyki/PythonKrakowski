import sys
import random
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMessageBox


class SaperGame(QWidget):
    def __init__(self, hub_window, rows=10, cols=10, num_snakes=10):
        super().__init__()

        self.setWindowIcon(QIcon("./assets/icon_pic.jpg"))
        self.hub_window = hub_window
        self.rows = rows
        self.cols = cols
        self.num_snakes = num_snakes
        self.snakes = set()
        self.flagged = set() 
        self.revealed = set()
        self.buttons = []
        self.setWindowTitle("Saper z Wężami")
        self.setGeometry(100, 100, 400, 400)

        self.init_ui()
        self.generate_snakes()

    def init_ui(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = QPushButton()
                button.setFixedSize(40, 40)
                button.setContextMenuPolicy(Qt.CustomContextMenu)
                button.customContextMenuRequested.connect(self.on_right_click)
                button.clicked.connect(self.on_button_click)
                self.layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)

    def generate_snakes(self):
        self.snakes.clear()
        while len(self.snakes) < self.num_snakes:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            self.snakes.add((row, col))

    def reset_game(self):
        self.flagged.clear()
        self.revealed.clear()
        self.generate_snakes()
        
        for row in range(self.rows):
            for col in range(self.cols):
                button = self.buttons[row][col]
                button.setEnabled(True)
                button.setText('')
                button.setStyleSheet("")

    def on_button_click(self):
        button = self.sender()
        pos = self.layout.getItemPosition(self.layout.indexOf(button))
        row, col = pos[0], pos[1]

        if (row, col) in self.flagged:
            return 

        if (row, col) in self.snakes:
            button.setText('🐍')
            button.setStyleSheet("background-color: red;")
            self.game_over()
        else:
            self.reveal_cell(row, col)
            self.check_win()

    def on_right_click(self, pos):
        button = self.sender()
        button_pos = self.layout.getItemPosition(self.layout.indexOf(button))
        row, col = button_pos[0], button_pos[1]

        if (row, col) in self.revealed:
            return

        if (row, col) in self.flagged:
            button.setText('')
            self.flagged.remove((row, col))
        else:
            button.setText('🚩')
            self.flagged.add((row, col))

    def adjacent_snakes(self, row, col):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        count = 0
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.rows and 0 <= c < self.cols and (r, c) in self.snakes:
                count += 1
        return count

    def reveal_cell(self, row, col):
        button = self.buttons[row][col]
        snake_count = self.adjacent_snakes(row, col)

        if snake_count == 0:
            button.setText('')
            button.setEnabled(False)
            self.revealed.add((row, col))

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in directions:
                r, c = row + dr, col + dc
                if 0 <= r < self.rows and 0 <= c < self.cols:
                    neighbor_button = self.buttons[r][c]
                    if neighbor_button.isEnabled() and (r, c) not in self.revealed:
                        self.reveal_cell(r, c)
        else:
            button.setText(str(snake_count))
            button.setEnabled(False)
            self.revealed.add((row, col))

    def check_win(self):
        total_cells = self.rows * self.cols
        non_snake_cells = total_cells - self.num_snakes
        if len(self.revealed) == non_snake_cells:
            self.game_win()

    def game_over(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = self.buttons[row][col]
                if (row, col) in self.snakes:
                    button.setText('🐍')
                    button.setStyleSheet("background-color: red;")
                button.setEnabled(False)
        self.show_restart_dialog("Przegrałeś! Chcesz zagrać jeszcze raz?")

    def game_win(self):
        for row in range(self.rows):
            for col in range(self.cols):
                button = self.buttons[row][col]
                if (row, col) in self.snakes:
                    button.setText('🐍')
                    button.setStyleSheet("background-color: green;")
                button.setEnabled(False)
        self.show_restart_dialog("Wygrałeś! Chcesz zagrać jeszcze raz?")

    def show_restart_dialog(self, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Koniec gry")
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        dialog.setDefaultButton(QMessageBox.Yes)
        choice = dialog.exec_()

        if choice == QMessageBox.Yes:
            self.reset_game()
        else:
            self.close()
            self.hub_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = SaperGame(None)
    game.show()
    sys.exit(app.exec_())