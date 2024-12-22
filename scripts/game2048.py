import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QLabel, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

GRID_SIZE = 4
INITIAL_TILES = 2
FONT = QFont("Arial", 20)

class Game2048(QMainWindow):
    def __init__(self, hub_window):
        super().__init__()
        self.hub_window = hub_window
        self.setWindowTitle("2048")
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)
        self.labels = [[QLabel("") for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                label = self.labels[i][j]
                label.setFont(FONT)
                label.setAlignment(Qt.AlignCenter)
                label.setFixedSize(100, 100)
                self.grid_layout.addWidget(label, i, j)
        
        self.spawn_tiles(INITIAL_TILES)
        self.update_grid()

    def spawn_tiles(self, count=1):
        self.validate_grid() 
        empty_positions = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        for _ in range(min(count, len(empty_positions))):
            i, j = random.choice(empty_positions)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4
            empty_positions.remove((i, j))

    def update_grid(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.grid[i][j]
                label = self.labels[i][j]
                label.setText("" if value == 0 else str(value))
                self.update_tile_color(label, value)

    def update_tile_color(self, label, value):
        palette = QPalette()
        if value == 0:
            palette.setColor(QPalette.Background, QColor(204, 192, 179))
        else:
            hue = (value.bit_length() * 35) % 360
            palette.setColor(QPalette.Background, QColor.fromHsv(hue, 150, 255))
        label.setAutoFillBackground(True)
        label.setPalette(palette)

    def keyPressEvent(self, event):
        key = event.key()
        moved = False

        if key == Qt.Key_Left:
            moved = self.move_left()
        elif key == Qt.Key_Right:
            moved = self.move_right()
        elif key == Qt.Key_Up:
            moved = self.move_up()
        elif key == Qt.Key_Down:
            moved = self.move_down()

        if moved:
            self.spawn_tiles()
            self.update_grid()
            if self.check_game_over():
                self.game_over()

    def slide_and_merge(self, line):
        new_line = [i for i in line if i != 0]
        for i in range(len(new_line) - 1):
            if new_line[i] == new_line[i + 1]:
                new_line[i] *= 2
                new_line[i + 1] = 0
        return [i for i in new_line if i != 0] + [0] * (GRID_SIZE - len(new_line))

    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            original = self.grid[i]
            self.grid[i] = self.slide_and_merge(self.grid[i])
            self.grid[i] = self.grid[i][:GRID_SIZE] + [0] * (GRID_SIZE - len(self.grid[i]))  # Ensure correct size
            if self.grid[i] != original:
                moved = True
        return moved

    def move_right(self):
        moved = False
        for i in range(GRID_SIZE):
            original = self.grid[i]
            self.grid[i] = self.slide_and_merge(self.grid[i][::-1])[::-1]
            self.grid[i] = self.grid[i][:GRID_SIZE] + [0] * (GRID_SIZE - len(self.grid[i]))  # Ensure correct size
            if self.grid[i] != original:
                moved = True
        return moved

    def move_up(self):
        moved = False
        for j in range(GRID_SIZE):
            original_column = [self.grid[i][j] for i in range(GRID_SIZE)]
            column = self.slide_and_merge(original_column)
            
            column += [0] * (GRID_SIZE - len(column))
            
            for i in range(GRID_SIZE):
                if self.grid[i][j] != column[i]:
                    moved = True
                self.grid[i][j] = column[i]
                
        return moved

    def move_down(self):
        moved = False
        for j in range(GRID_SIZE):
            original_column = [self.grid[i][j] for i in range(GRID_SIZE)]
            column = self.slide_and_merge(original_column[::-1])[::-1]
            
            column = [0] * (GRID_SIZE - len(column)) + column
            
            for i in range(GRID_SIZE):
                if self.grid[i][j] != column[i]:
                    moved = True
                self.grid[i][j] = column[i]
                
        return moved


    def check_game_over(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
                if j < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
                if i < GRID_SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        return True

    def game_over(self):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Koniec gry!")
        msg_box.setText("Koniec gry! Chcesz zagrać ponownie?")
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        reply = msg_box.exec_()
        
        if reply == QMessageBox.Yes:
            self.setWindowTitle("2048 - Wężowy Motyw")
            self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
            self.spawn_tiles(INITIAL_TILES)
            self.update_grid()
        elif reply == QMessageBox.No:
            self.close()
            self.hub_window.show()

    def validate_grid(self):
        if len(self.grid) != GRID_SIZE or any(len(row) != GRID_SIZE for row in self.grid):
            print("Invalid grid detected:", self.grid)
            raise ValueError("Grid dimensions are incorrect!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game2048(None)
    game.show()
    sys.exit(app.exec_())
