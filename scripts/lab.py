from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QWidget, QRadioButton, QDialog, QDialogButtonBox, QMessageBox
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QRect
import random
import sys

class ModeSelectionDialog(QDialog):
    def __init__(self, hub_window):
        super().__init__()
        self.hub_window = hub_window
        self.setWindowTitle("Wybór trybu gry")
        self.setGeometry(100, 100, 300, 150)

        self.normal_mode_radio = QRadioButton("Normalny tryb", self)
        self.fog_of_war_radio = QRadioButton("Mgła wojny", self)
        self.fog_of_war_radio.setChecked(True)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addWidget(self.normal_mode_radio)
        layout.addWidget(self.fog_of_war_radio)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def selected_mode(self):
        if self.normal_mode_radio.isChecked():
            return 'normal'
        else:
            return 'fog_of_war'

    def get_hub_window(self):
        return self.hub_window
    
class LabirynthGame(QMainWindow):
    def __init__(self, game_mode, hub_window):
        super().__init__()
        self.game_mode = game_mode 
        self.init_ui()
        self.hub_window = hub_window

    def init_ui(self):
        self.grid_size = 30 
        self.cell_size = 30  

        window_width = self.grid_size * self.cell_size
        window_height = self.grid_size * self.cell_size + 50 

        self.setWindowTitle("Labirynt - Wąż")
        self.setGeometry(100, 100, window_width, window_height)
        self.setFixedSize(window_width - self.cell_size, window_height - self.cell_size) 

        self.steps = 0 
        self.snake_pos = [1, 1] 
        self.goal_pos = [self.grid_size - 2, self.grid_size - 2]  

        self.generate_maze()

        self.status_bar = QLabel(f"Kroki: {self.steps}", self)
        self.status_bar.setAlignment(Qt.AlignCenter)
        self.status_bar.setStyleSheet("font-size: 20px; font-weight: bold;")  

        maze_layout = QVBoxLayout()
        maze_widget = QWidget(self)
        maze_widget.setLayout(maze_layout)

        maze_layout.addStretch(1) 

        main_layout = QVBoxLayout()
        main_layout.addWidget(maze_widget)
        main_layout.addWidget(self.status_bar)  

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.show()

    def generate_maze(self):
        self.grid_size -= 1 
        self.maze = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for i in range(self.grid_size):
            self.maze[i][self.grid_size - 1] = 0
            self.maze[self.grid_size - 1][i] = 0

        self.maze[1][1] = 1  
        self.carve_passages(1, 1)

        while True:
            goal_x = random.randint(1, self.grid_size - 2)  
            goal_y = random.randint(1, self.grid_size - 2)

            if self.maze[goal_y][goal_x] == 1 and self.is_end_of_corridor(goal_x, goal_y):
                self.goal_pos = [goal_y, goal_x]
                break

        while True:
            snake_x = random.randint(1, self.grid_size - 2)
            snake_y = random.randint(1, self.grid_size - 2)

            if self.maze[snake_y][snake_x] == 1 and [snake_y, snake_x] != self.goal_pos and self.is_end_of_corridor(snake_x, snake_y):
                self.snake_pos = [snake_y, snake_x]
                break

    def carve_passages(self, cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if 1 <= nx < self.grid_size - 1 and 1 <= ny < self.grid_size - 1 and self.maze[ny][nx] == 0:
                self.maze[cy + dy][cx + dx] = 1
                self.maze[ny][nx] = 1
                self.carve_passages(nx, ny)

    def is_end_of_corridor(self, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        passage_count = 0

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and self.maze[ny][nx] == 1:
                passage_count += 1

        return passage_count == 1

    def paintEvent(self, event):
        painter = QPainter(self)

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.game_mode == 'fog_of_war' and (abs(self.snake_pos[0] - y) > 1 or abs(self.snake_pos[1] - x) > 1):
                    color = QColor("black") 
                else:
                    if self.maze[y][x] == 0:
                        color = QColor("black")
                    else:
                        color = QColor("white")

                if [y, x] == self.snake_pos:
                    color = QColor("green")

                painter.fillRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, color)
                painter.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

        painter.setBrush(QColor("red"))
        goal_rect = QRect(self.goal_pos[1] * self.cell_size, self.goal_pos[0] * self.cell_size, self.cell_size, self.cell_size)
        painter.fillRect(goal_rect, QColor("red"))
        painter.drawRect(goal_rect)

    def keyPressEvent(self, event):
        key = event.key()
        new_pos = self.snake_pos[:]

        if key == Qt.Key_Up:
            new_pos[0] -= 1
        elif key == Qt.Key_Down:
            new_pos[0] += 1
        elif key == Qt.Key_Left:
            new_pos[1] -= 1
        elif key == Qt.Key_Right:
            new_pos[1] += 1
        else:
            return

        if 0 <= new_pos[0] < self.grid_size and 0 <= new_pos[1] < self.grid_size and self.maze[new_pos[0]][new_pos[1]] == 1:
            self.snake_pos = new_pos
            self.steps += 1
            self.status_bar.setText(f"Kroki: {self.steps}")

            if self.snake_pos == self.goal_pos:
                self.status_bar.setText(f"Udało się! Kroki: {self.steps}")
                self.show_win_dialog()

        self.update()

    def show_win_dialog(self):
        reply = QMessageBox.question(self, 'Wygrałeś!',
                                     f"Wąż zrobił {self.steps} kroków. Czy chcesz zagrać jeszcze raz?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.reset_game()
        else:
            self.close()
            self.hub_window.show()

    def reset_game(self):
        mode_dialog = ModeSelectionDialog()
        self.close() 
        if mode_dialog.exec_() == QDialog.Accepted:
            game_mode = mode_dialog.selected_mode()
            self.game = LabirynthGame(game_mode)
            self.game.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    mode_dialog = ModeSelectionDialog(None)
    if mode_dialog.exec_() == QDialog.Accepted:
        game_mode = mode_dialog.selected_mode()
        game = LabirynthGame(game_mode, mode_dialog.get_hub_window())
        game.show()

    sys.exit(app.exec_())
