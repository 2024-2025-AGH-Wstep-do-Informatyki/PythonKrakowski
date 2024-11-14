# 🐍 PyHUB 🐍

## 📝 Opis Programu 📝

Nasz projekt to hub z prostymi grami stworzonymi w Pythonie za pomocą PyQt5, gdzie głównym motywem jest wąż. Planowo każda gra w hubie będzie zawierać elementy związane z wężami, nawiązując do języka programowania Python.

## 💻 Używane Technologie 💻

<p>
  <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PyQt5-%2523217346.svg?style=for-the-badge&logo=Qt&logoColor=white&color=%233366ff" />
  <img src="https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white" />
  <img src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=codecrafters&logoColor=white" />
</p>

## 🎮 Dostępne Gry 🎮

1. **Snake 🐍** – Klasyczna gra, w której użytkownik steruje wężem, aby zbierał jedzenie i rósł w rozmiarze. Gracz musi unikać kolizji z własnym ogonem oraz ścianami, aby jak najdłużej przetrwać.
2. **Dino Snake 🦖🐍** – Alternatywa dla tradycyjnej gry Dino Game, gdzie dinozaur zostaje zastąpiony przez skaczącego węża, który musi unikać przeszkód w trakcie biegu. (Gra nie ma jeszcze grafik związanych z wężami)
3. **Tic-Tac-Toe Snake 🐍⭕❌** – Gra w kółko i krzyżyk z motywem węża, gdzie plansza oraz symbole będą stylizowane na temat wężowy. (W chwili obecnej dostępna zwykła wersja)
4. **Snake Minesweeper 🐍💣** – Wersja klasycznego Saper z nowym motywem: zamiast min, na planszy znajdują się węże! Celem gry jest odkrycie wszystkich bezpiecznych pól na planszy, unikając kontaktu z wężami.
5. **Snake Minesweeper 🐍💀🎯** – Gra w wisielca z motywem węża zamiast szubienicy: Po każdym nietrafionym strzale dorysowywane są kolejne części węża. Celem gry jest odgadnięcie słowa wylosowanego przez program (gra nie obsługuje słów z polskimi znakami)

## ⚙️ Instrukcja Uruchamiania ⚙️

Aby uruchomić hub gier w Pythonie z PyQt5, wykonaj poniższe kroki:

#### 🐍 Krok 1: Zainstaluj Python 🐍

Upewnij się, że masz zainstalowaną najnowszą wersję Pythona (3.x). Możesz ją pobrać ze strony [python.org](https://www.python.org/). Podczas instalacji upewnij się, że zaznaczyłeś opcję „Add Python to PATH”.

#### 🖥️ Krok 2: Zainstaluj PyQt5 🖥️

Projekt wymaga biblioteki PyQt5, która jest używana do tworzenia interfejsu użytkownika. Zainstaluj ją, uruchamiając następujące polecenie w terminalu:

```bash
pip install PyQt5
```

#### 📥 Krok 3: Pobierz pliki projektu 📥

Pobierz pliki projektu na swój komputer. Projekt jest dostępny na GitHubie, więc możesz sklonować go przy użyciu:

```bash
git clone https://github.com/2024-2025-AGH-Wstep-do-Informatyki/PythonKrakowski.git
```

lub po prostu pobierz pliki i rozpakuj je w wybranym folderze.

#### 🚀 Krok 4: Uruchom hub gier 🚀

Przejdź do folderu projektu w terminalu, a następnie uruchom główny plik huba:

```bash
python game_hub.py
```

Główne okno huba otworzy się, a Ty będziesz mógł wybrać jedną z dostępnych gier.

#### 🕹️ Krok 5: Wybierz grę 🕹️

W oknie huba kliknij na nazwę gry, którą chcesz uruchomić. Każda gra otworzy się w osobnym oknie, a hub automatycznie zamknie się. Miłej rozgrywki! 🎉
