from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QHeaderView, QMessageBox
from PyQt5.Qt import Qt
from PyQt5.QtGui import QFont, QColor, QFontDatabase
import random
import sys

class SudokuGame(QMainWindow):
    def __init__(self, return_to_hub_callback):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setGeometry(200, 200, 600, 700)

        self.return_to_hub_callback = return_to_hub_callback
        self.board = generate_sudoku()
        self.solved_board = [row[:] for row in self.board]  
        solve_sudoku(self.solved_board)  
        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        font_id = QFontDatabase.addApplicationFont("./assets/sudoku/SnakeChan.ttf")
        snake_font = QFontDatabase.applicationFontFamilies(font_id)

        main_layout = QVBoxLayout(central_widget)

        self.table = QTableWidget(9, 9)
        self.table.setFont(QFont(snake_font[0], 28))
        self.table.setStyleSheet("QTableWidget { color: #31e00d; }") 
        self.table.setEditTriggers(QTableWidget.AllEditTriggers)
        main_layout.addWidget(self.table)

        self.table.horizontalHeader().setVisible(False)
        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        button_layout = QHBoxLayout()

        check_button = QPushButton("Sprawdź rozwiązanie", self)
        check_button.clicked.connect(self.check_solution)
        button_layout.addWidget(check_button)

        new_game_button = QPushButton("Nowa zagadka", self)
        new_game_button.clicked.connect(self.new_game)
        button_layout.addWidget(new_game_button)

        solve_button = QPushButton("Pokaż rozwiązanie", self)
        solve_button.clicked.connect(self.show_solution)
        button_layout.addWidget(solve_button)

        back_button = QPushButton("Powrót do menu", self)
        back_button.clicked.connect(self.return_to_hub)
        button_layout.addWidget(back_button)

        main_layout.addLayout(button_layout)

        self.load_board()

    def load_board(self):
        for i in range(9):
            for j in range(9):
                item = QTableWidgetItem()
                if self.board[i][j] != 0:
                    item.setText(str(self.board[i][j]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                else:
                    item.setFlags(item.flags() | Qt.ItemIsEditable) 

                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

    def check_solution(self):
        solved = True 
        empty_found = False

        for row in range(9):
            for col in range(9):
                item = self.table.item(row, col)
                
                num = int(item.text()) if item.text() != "" else 0

                if num == 0:
                    empty_found = True 
                if num != self.solved_board[row][col]: 
                    item.setBackground(QColor("red")) 
                    solved = False
                else:
                    item.setBackground(QColor("white")) 

        if empty_found:
            self.show_message("Puste pole!", "Zostawiłeś puste pole. Wypełnij wszystkie komórki przed sprawdzeniem rozwiązania.")
        elif solved:
            self.show_message("Gratulacje!", "Rozwiązałeś sudoku poprawnie!")
        else:
            self.show_message("Błąd!", "Niektóre odpowiedzi są niepoprawne. Spróbuj ponownie.")

    def show_message(self, title, text):
        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setIcon(QMessageBox.Information if "Gratulacje" in title else QMessageBox.Critical)
        message_box.exec_()

    def new_game(self):
        self.board = generate_sudoku()
        self.solved_board = [row[:] for row in self.board]
        solve_sudoku(self.solved_board) 
        self.load_board()

    def show_solution(self):
        for i in range(9):
            for j in range(9):
                item = self.table.item(i, j)
                if item is not None:
                    
                    if self.board[i][j] == 0:
                        item.setText(str(self.solved_board[i][j])) 
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable) 
                        item.setBackground(QColor("white"))
                    else:
                        item.setBackground(QColor("white"))


    def return_to_hub(self):
        self.close()
        self.return_to_hub_callback()

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
