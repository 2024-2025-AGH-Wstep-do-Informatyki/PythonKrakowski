a1 = " "
a2 = " "
a3 = " "
b1 = " "
b2 = " "
b3 = " "
c1 = " "
c2 = " "
c3 = " "

### board display
def board():  
    print("-------------------------")
    
    for i in range(4):
        print("|       ", end="")
    print("")

    print("|", a1, sep="   ", end="   ")
    print("|", a2, sep="   ", end="   ")
    print("|", a3, sep="   ", end="   ")
    print("|")

    for i in range(4):
        print("|       ", end="")
    print("")

    print("-------------------------")
    
    for i in range(4):
        print("|       ", end="")
    print("")

    print("|", b1, sep="   ", end="   ")
    print("|", b2, sep="   ", end="   ")
    print("|", b3, sep="   ", end="   ")
    print("|")

    for i in range(4):
        print("|       ", end="")
    print("")

    print("-------------------------")
    
    for i in range(4):
        print("|       ", end="")
    print("")

    print("|", c1, sep="   ", end="   ")
    print("|", c2, sep="   ", end="   ")
    print("|", c3, sep="   ", end="   ")
    print("|")

    for i in range(4):
        print("|       ", end="")
    print("")

    print("-------------------------")
    
board()

print("Welcome to the tic-tac-toe game!")
print("Tiels are numbered from top-left to bottom-right (a1, a2, a3, b1, b2, b3, c1, c2, c3)")
print("\ncircle starts")

while True:
    choose = input("Choose tiel to start: ")

    if choose == "a1":
        a1 = "o"
        break
    elif choose == "a2":
        a2 = "o"    
        break
    elif choose == "a3":
        a3 = "o"  
        break
    elif choose == "b1":
        b1 = "o" 
        break
    elif choose == "b2":
        b2 = "o"  
        break
    elif choose == "b3":
        b3 = "o"  
        break
    elif choose == "c1":
        c1 = "o"  
        break
    elif choose == "c2":
        c2 = "o"  
        break
    elif choose == "c3":
        c3 = "o" 
        break
    else:
        print("Wrong input, try again!")

board()

### insert o
def asko():
    global a1, a2, a3, b1, b2, b3, c1, c2, c3
    while True:
        choose = input("Choose next tiel for o: ")

        if choose == "a1":
            if a1 == " ":
                a1 = "o"
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "a2":
            if a2 == " ":
                a2 = "o"    
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "a3":
            if a3 == " ":
                a3 = "o"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "b1":
            if b1 == " ":
                b1 = "o" 
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "b2":
            if b2 == " ":
                b2 = "o"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "b3":
            if b3 == " ":
                b3 = "o"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "c1":
            if c1 == " ":
                c1 = "o"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "c2":
            if c2 == " ":
                c2 = "o"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "c3":
            if c3 == " ":
                c3 = "o" 
                break
            else:
                print("Tiel occupied, try again!")
                continue
        else:
            print("Wrong input, try again!")
        
    board()

### insert x
def askx():
    global a1, a2, a3, b1, b2, b3, c1, c2, c3
    while True:
        choose = input("Choose next tiel for x: ")

        if choose == "a1":
            if a1 == " ":
                a1 = "x"
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "a2":
            if a2 == " ":
                a2 = "x"    
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "a3":
            if a3 == " ":
                a3 = "x"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "b1":
            if b1 == " ":
                b1 = "x" 
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "b2":
            if b2 == " ":
                b2 = "x"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "b3":
            if b3 == " ":
                b3 = "x"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "c1":
            if c1 == " ":
                c1 = "x"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "c2":
            if c2 == " ":
                c2 = "x"  
                break
            else:
                print("Tiel occupied, try again!")
                continue
        elif choose == "c3":
            if c3 == " ":
                c3 = "x" 
                break
            else:
                print("Tiel occupied, try again!")
                continue
        else:
            print("Wrong input, try again!")

    board()

### check if x win
def ifwinx():
    global a1, a2, a3, b1, b2, b3, c1, c2, c3
    if a1 == a2 == a3 == "x":
        print("x won!")
        exit()
    elif b1 == b2 == b3 == "x":
        print("x won!")
        exit()
    elif c1 == c2 == c3 == "x":
        print("x won!")
        exit()
    elif a1 == b1 == c1 == "x":
        print("x won!")
        exit()
    elif a2 == b2 == c2 == "x":
        print("x won!")
        exit()
    elif a3 == b3 == c3 == "x":
        print("x won!")
        exit()
    elif a1 == b2 == c3 == "x":
        print("x won!")
        exit()
    elif c1 == b2 == a3 == "x":
        print("x won!")
        exit()

### check if o win
def ifwino():
    global a1, a2, a3, b1, b2, b3, c1, c2, c3
    if a1 == a2 == a3 == "o":
        print("o won!")
        exit()
    elif b1 == b2 == b3 == "o":
        print("o won!")
        exit()
    elif c1 == c2 == c3 == "o":
        print("o won!")
        exit()
    elif a1 == b1 == c1 == "o":
        print("o won!")
        exit()
    elif a2 == b2 == c2 == "o":
        print("o won!")
        exit()
    elif a3 == b3 == c3 == "o":
        print("o won!")
        exit()
    elif a1 == b2 == c3 == "o":
        print("o won!")
        exit()
    elif c1 == b2 == a3 == "o":
        print("o won!")
        exit()
        
for n in range(4):
    askx()
    ifwino()
    ifwinx()
    asko()
    ifwino()
    ifwinx()

print("Draw!")