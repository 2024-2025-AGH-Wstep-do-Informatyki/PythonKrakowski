import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import  QFont, QPalette, QColor

class TicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kółko-krzyżyk")
        self.setGeometry(100, 100, 300, 320)

        self.board = [['' for _ in range(3)] for _ in range(3)]                     #atrybuty gry: plansza, gracze, informacja o tym czy gra się zakończyła
        self.current_player = 'X'
        self.game_over = False
        self.init_ui()                                                              #interfejs użytkownika (planszy)

    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        layout = QGridLayout(self.central_widget)                                   #layout do rozmieszczenia przycisków w siatce
        self.buttons = [[QPushButton('') for _ in range(3)] for _ in range(3)]      #utworzenie przycisków na planszy
        for i in range(3):
            for j in range(3):
                button = self.buttons[i][j]                                         #ustawienie rozmirów przycisków, rozmiarów czcionki i koloru z jakimi będą wyświetlane 'X' i 'O'
                button.setStyleSheet("background-color: blue")
                button.setFixedSize(70, 70)
                button.setStyleSheet("font-size: 60px; color: blue") 
                button.clicked.connect(self.on_click(i, j))                         #łączy przyciski z "akcją" kliknięcia
                layout.addWidget(button, i, j)

        self.info_label = QLabel(self)                                              #etykieta informująca o aktualnym graczu, wygranym albo remisie
        self.info_label.setStyleSheet("color: black; font-size: 15px")
        self.info_label.setText(f"Gracz {self.current_player} rozpoczyna")
        self.info_label.setAlignment(Qt.AlignCenter)                                #ustawia etykiete info_label, na środku ekranu na dole
        layout.addWidget(self.info_label, 3, 0, 1, 3)

    def on_click(self, row, col):
        def handler():
            if self.game_over == False:
                if self.board[row][col] == '':                                      #sprawdzam, czy pole jest puste (czy gracz może je wybrać)
                    self.board[row][col] = self.current_player                      #ustawia SYMBOL bieżacego gracza (bez tego wiersza byłyby widoczne 'X' i 'O', ale jakby nie byłyby widoczne dla programu)
                    self.buttons[row][col].setText(self.current_player)             #ustawia TEKST bieżacego gracza (bez tego wiersza 'X' i 'O' nie byłyby widoczne dla graczy)

                if self.check_win():                                                #sprawdzenie, czy ktoś wygrał po tej turze
                    self.info_label.setText(f"Gracz {self.current_player} wygrał!")
                    self.game_over = True
                    self.show_end_screen(self.current_player)
                
                elif self.check_draw():                                             #sprawdzenie, czy po tej turze jest remis
                    self.info_label.setText("Remis!")
                    self.game_over = True
                    self.show_end_screen("Remis")
                
                else:                                                               #zmiana gracza
                    self.current_player = 'O' if self.current_player == 'X' else 'X'
                    self.info_label.setText(f"Tura gracza {self.current_player}")
        return handler
        

    def check_win(self):
        #jeżeli wszytskie kwadraciki w jednym wierszu, kolumnie lub przekątnej mają tą samą wartość różną od 0 to znaczy, że gre wygrał obecny gracz, 
        #dlatego nie trzeba rozpatrywać osobnych przypadków dla 'X' i 'O'
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '':
                return True
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '':
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '':
            return True

        return False

    def check_draw(self):
        #jeżeli na planszy nie ma już żadnego wolnego pola to znaczy, że jest remis
        #(jeżeli, któryś cała plansza jest zapełniona, ale któryś z graczy wygrał to zostało to sprawdzone przez funkcje check_win)
        for i in range(3):
            for j in range(3):
                if self.board[j][i] == '':
                    return False
        return True

    def show_end_screen(self, winner):                                                  #czyści plansze i wyświetla informacje o wyniku
        self.clear_board()                                                             

        if winner == "Remis":
            self.info_label.setStyleSheet("color: red; font-size: 15px")
            self.info_label.setText("Remis!")
        else:
            self.info_label.setStyleSheet("color: red; font-size: 15px")
            self.info_label.setText(f"Gracz {winner} wygrał!")
        
        self.restart_ask()                                                              #okno dialogowe z pytaniem, czy gracze chcą grać ponownie

    def restart_ask(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Koniec gry")
        msg.setText("Czy chcesz zagrać ponownie?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        if msg.exec_() == QMessageBox.Yes:
            self.game_restart()
        else:
            self.close() 

    def game_restart(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]                         #ponowne ustawienie atrybutów gry
        self.current_player = 'X'
        self.game_over = False

        
        for row in self.buttons:                                                        #czyszczenie planszy po poprzedniej grze
            for button in row:
                button.setText('')
                button.setEnabled(True)                                                 #włączenie przycisków na nowo
        
        self.info_label.setStyleSheet("color: black; font-size: 15px")
        self.info_label.setText(f"Nowa gra. Gracz {self.current_player} rozpoczyna")

    def clear_board(self):
        """ Wyczyść planszę z przycisków """
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)                                                #zablokowanie przycisków po zakończeniu gry

def main():
    app = QApplication(sys.argv)
    game = TicTacToe()
    game.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

