"""

by TeamCoder | Bielefeld
Special Thanks to Danny

"""

import random
from array import *
from time import sleep
import turtle

#Global Variables
SIZE = (301, 301)
#SIZE = (31, 31) #for visualization purposes
NB_HUMANS = 45000
#NB_HUMANS = 300 #for visualization purposes
NB_DAYS = 6000
#NB_DAYS = 1000
NB_SRT = 5
NB_CURRENT_ZOMBIES = 0
NB_CURRENT_HUMANS = 0
NB_CURRENT_DAY = 0
NB_CHECKING_RANDOM_NB = 100
NB_DAYS_TO_GET_HUNGRY = 4
#vorrat_holen = 0

#Defining of the values in the matrix
ENC_NULL = 0
ENC_HUMAN = (1003, 1999, 1009)
ENC_ZOMBIE = (2000, 2030)

assert NB_HUMANS - 1 < SIZE[0]*SIZE[1]

def check_zombie(x, y):
    if MAP[x][y] >= ENC_ZOMBIE[0] and MAP[x][y] <= ENC_ZOMBIE[1]:
        return True

def check_human(x, y):
    is_human, is_visible = False, False
    if MAP[x][y] >= ENC_HUMAN[0] and MAP[x][y] <= ENC_HUMAN[1]:
        is_human = True
    if MAP[x][y] >= ENC_HUMAN[0] and MAP[x][y] <= ENC_HUMAN[2]:
        is_visible = True
    return is_human, is_visible

# Generation of the matrix
def generate_matrix():  #Generate Map
    global MAP, ENC_HUMAN, ENC_ZOMBIE, ENC_NULL
    MAP = []
    for i in range(SIZE[0]):
            MAP.append([0 for i in range(SIZE[1])])


    for i in range(NB_HUMANS):
        for j in range(NB_CHECKING_RANDOM_NB):
            x, y = SIZE[0]//2+random.randint(0,SIZE[0]//2)-random.randint(0,SIZE[0]//2), SIZE[1]//2+random.randint(0,SIZE[1]//2)-random.randint(0,SIZE[1]//2)
            if check_human(x, y)[0]:
                continue
            break
        MAP[x][y] = 1007
        #MAP[x][y] = 1009
    print("OMG")
    MAP[SIZE[0]//2][SIZE[1]//2] = ENC_ZOMBIE[1]


def show_map():
    for i in MAP:
        print(i)


#Functions of the loop
def check_state(PRINT=True, all_=True):
    global NB_CURRENT_HUMANS, NB_CURRENT_ZOMBIES
    NB_CURRENT_HUMANS, NB_CURRENT_ZOMBIES = 0, 0
    for x in range(SIZE[0]):
        for y in range(SIZE[1]):
            if check_human(x, y)[0]:
                NB_CURRENT_HUMANS += 1
            elif check_zombie(x, y):
                NB_CURRENT_ZOMBIES += 1
    if PRINT:
        print(f"Zombies: {NB_CURRENT_ZOMBIES}\nMenschen: {NB_CURRENT_HUMANS}")
        if all_:
            print(f'At all there are now {NB_CURRENT_ZOMBIES+NB_CURRENT_HUMANS} things')
        print('\n')
    

def zombie_step():  #Zombies: Infect
    global MAP
    places_to_infect = []
    for x in range(SIZE[0]):
        for y in range(SIZE[1]):
            if check_zombie(x, y) and MAP[x][y] > ENC_ZOMBIE[1] - NB_DAYS_TO_GET_HUNGRY*NB_SRT:
                if x < 300:
                    if check_human(x + 1, y)[1]:
                        places_to_infect.append((x + 1, y))
                if x > 0:
                    if check_human(x - 1, y)[1]:
                        places_to_infect.append((x - 1, y))
                if y < 300:
                    if check_human(x, y + 1)[1]:
                        places_to_infect.append((x, y + 1))
                if y > 0:
                    if check_human(x, y - 1)[1]:
                        places_to_infect.append((x, y - 1))
                if len(places_to_infect) > 0:
                    choice = random.choice(places_to_infect)
                    MAP[choice[0]][choice[1]] = ENC_ZOMBIE[1]


def go():   #Zombies: Go
    global MAP
    for x in range(SIZE[0]):
        for y in range(SIZE[1]):
            if check_zombie(x, y):
                zufall = ["links", "rechts", "oben", "unten"]
                choice = random.choice(zufall)
                if choice == "links" and x > 0:
                    if MAP[x - 1][y] == ENC_NULL:
                        MAP[x - 1][y] = MAP[x][y]
                        MAP[x][y] = 0
                elif choice == "rechts" and x < 300:
                    if MAP[x + 1][y] == ENC_NULL:
                        MAP[x + 1][y] = MAP[x][y]
                        MAP[x][y] = 0
                elif choice == "oben" and y > 0:
                    if MAP[x][y - 1] == ENC_NULL:
                        MAP[x][y - 1] = MAP[x][y]
                        MAP[x][y] = 0
                elif choice == "unten" and y < 300:
                    if MAP[x][y + 1] == ENC_NULL:
                        MAP[x][y + 1] = MAP[x][y]
                        MAP[x][y] = 0


def update_zombie_lifes():
    for x in range(SIZE[0]):
        for y in range(SIZE[1]):
            if check_zombie(x, y):
                MAP[x][y] -= 1
                if MAP[x][y] == ENC_ZOMBIE[0]:
                    MAP[x][y] = 0

def update_visible():
    global MAP
    #global vorrat_holen
    for x in range(SIZE[0]):
        for y in range(SIZE[1]):
            if check_human(x, y)[0]:
                if MAP[x][y] < 1004 and NB_CURRENT_DAY >= 0 and NB_CURRENT_DAY <= 17:
                    MAP[x][y] = random.randint(1050, 1110)
                elif MAP[x][y] < 1004 and NB_CURRENT_DAY >= 18 and NB_CURRENT_DAY <= 29:
                    MAP[x][y] = random.randint(1010,1040)
                    #vorrat_holen += 1
                elif MAP[x][y] < 1004 and NB_CURRENT_DAY >= 30:
                    MAP[x][y] = random.randint(1010,1025)
                   # vorrat_holen += 1
                #elif MAP[x][y] < 1004 and vorrat_holen >= 3:
                 #   MAP[x][y] = random.randint(1030, 1055)

                #  vorrat_holen += 1
                else:
                    MAP[x][y] -= 1
                #elif vorrat_holen == 4 and MAP[x][y] < 1004:
                 #   MAP[x][y] = 1005
                #elif MAP[x][y] == 1000:
                 #   MAP[x][y] = 0
            
        
def zombies_eat():  #Zombies: Eat
    global MAP
    places_to_eat = []
    for x in range(SIZE[0]):
        for y in range(SIZE[1]):
            if check_zombie(x, y) and MAP[x][y] <= ENC_ZOMBIE[1] - NB_DAYS_TO_GET_HUNGRY*NB_SRT:
                if x < 300:
                    if check_human(x + 1, y)[1] or check_zombie(x + 1, y):
                        places_to_eat.append((x + 1, y))
                if x > 0:
                    if check_human(x - 1, y)[1] or check_zombie(x - 1, y):
                        places_to_eat.append((x - 1, y))
                if y < 300:
                    if check_human(x, y + 1)[1] or check_zombie(x, y + 1):
                        places_to_eat.append((x, y + 1))
                if y > 0:
                    if check_human(x, y - 1)[1] or check_zombie(x, y - 1):
                        places_to_eat.append((x, y - 1))
                if len(places_to_eat) > 0:
                    choice = random.choice(places_to_eat)
                    MAP[choice[0]][choice[1]] = ENC_NULL
                    MAP[x][y] = ENC_ZOMBIE[1]


def visualize(mysize=2):    #map
    turtle.speed(0)
    turtle.tracer(0, 0)
    turtle.goto(-150, 150)
    for y in range(SIZE[0]):
        for x in range(SIZE[1]):
            if check_zombie(x, y):
                turtle.color("Green")
                turtle.forward(mysize)
            elif check_human(x, y)[0]:
                turtle.color("Blue")
                turtle.forward(mysize)
            elif MAP[x][y] == ENC_NULL:
                turtle.color("Black")
                turtle.forward(mysize)
        turtle.right(90)
        turtle.forward(mysize/2)
        turtle.right(90)
        for j in range(SIZE[1]):
            if check_zombie(x, y):
                turtle.color("Green")
                turtle.forward(mysize)
            elif check_human(x, y)[0]:
                turtle.color("Blue")
                turtle.forward(mysize)
            elif MAP[x][y] == ENC_NULL:
                turtle.color("Black")
                turtle.forward(mysize)
        turtle.left(90)
        turtle.forward(mysize/2)
        turtle.left(90)
        if y%5 == 0:
            turtle.update()
    turtle.update()



def step(j, i):
    zombie_step()
    zombies_eat()
    go()
    update_zombie_lifes()
    update_visible()
    if i % 100 == 0 and j == 0:
        print(i)
        visualize()



#Game loop
def game_loop(verbose=1, all_=True):
    generate_matrix()
    j = 0
    for i in range(NB_DAYS):
        if verbose >= 1:
            print(f'Day {i}')
            check_state(PRINT=True, all_=all_)

        
        for j in range(NB_SRT):
            if verbose >= 2:
                print(f'Day {i}, Round {j}')
                check_state(PRINT=True, all_=all_)
            step(j, i)
            if NB_CURRENT_ZOMBIES == 0:
                print("Die Menschen haben gewonnen!")
            elif NB_CURRENT_HUMANS == 0:
                print("Die Zombies haben gewonnen!")
    print('At the end:')
    check_state(PRINT=True, all_=all_)

if __name__ == '__main__':
    game_loop(verbose=1, all_=True)
