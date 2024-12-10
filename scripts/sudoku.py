from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, 
    QWidget, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt5.Qt import Qt
from PyQt5.QtGui import QFont
import random
import sys


class SudokuGame(QMainWindow):
    def __init__(self, return_to_hub_callback):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setGeometry(200, 200, 600, 700)

        self.return_to_hub_callback = return_to_hub_callback
        self.board = generate_sudoku()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.table = QTableWidget(9, 9)
        self.table.setFont(QFont("Arial", 16))
        self.table.setFixedSize(540, 540)
        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("gridline-color: black;")
        self.load_board()

        layout.addWidget(self.table)

        # Buttons
        buttons_layout = QHBoxLayout()
        self.check_button = QPushButton("Sprawdź")
        self.check_button.clicked.connect(self.check_solution)
        self.return_button = QPushButton("Powrót do Huba")
        self.return_button.clicked.connect(self.return_to_hub)

        buttons_layout.addWidget(self.check_button)
        buttons_layout.addWidget(self.return_button)
        layout.addLayout(buttons_layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_board(self):
        for i in range(9):
            for j in range(9):
                item = QTableWidgetItem()
                if self.board[i][j] != 0:
                    item.setText(str(self.board[i][j]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable) 
                self.table.setItem(i, j, item)

    def check_solution(self):
        for row in range(9):
            for col in range(9):
                item = self.table.item(row, col)
                if item is None or not item.text().isdigit():
                    self.show_message("Niepoprawne rozwiązanie! Puste pola lub brak liczb.")
                    return

                num = int(item.text())
                if not is_valid(self.board, row, col, num):
                    self.show_message("Niepoprawne rozwiązanie! Powtarzające się liczby.")
                    return

        self.show_message("Gratulacje! Rozwiązałeś Sudoku poprawnie.")

    def return_to_hub(self):
        self.close()
        self.return_to_hub_callback()

    def show_message(self, message):
        QMessageBox.information(self, "Sudoku", message)

def generate_sudoku():
    board = [[0 for _ in range(9)] for _ in range(9)]
    fill_diagonal_boxes(board)
    solve_sudoku(board)
    remove_numbers(board)
    return board

def fill_diagonal_boxes(board):
    for i in range(0, 9, 3):
        fill_box(board, i, i)

def fill_box(board, row, col):
    nums = random.sample(range(1, 10), 9)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums.pop()

def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def remove_numbers(board):
    attempts = 50
    while attempts > 0:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if board[row][col] != 0:
            board[row][col] = 0
            attempts -= 1

if __name__ == "__main__":
    app = QApplication(sys.argv)

    def return_to_hub_stub():
        print("Returning to hub...")

    window = SudokuGame(return_to_hub_stub)
    window.show()

    sys.exit(app.exec_())
