import random
import pyxel
import math
# taille de la fenetre 128x128 pixels
# ne pas modifier
catlist = []
# position initiale du vaisseau
# (origine des positions : coin haut gauche)
MENU_BTN_POS = (118, 5)
MENU_BTN_SIZE = (5, 5)
WINDOW_SIZE = (128, 128)
pyxel.init(128, 128, title="Nuit du c0de 2024 : Chat Jeu")

pyxel.mouse(True)
maxcapacity = 0
bitcoins = 10


class ShopObject:

    def __init__(self, name, level, price):
        # !!! USING **KWARGS WOULD BE BETTER !!!
        self.name = name
        self.level = level
        self.price = price
        
        self.color = level
       
        self.x = 0
        self.y = 0
       
        self.bought = False


class Shop:
   
    def __init__(self, objects):
        self._objects = list(objects)
       
        self.is_displayed = False
   
    def add_objects(self, list):
        list = list(list)
        for object in list:
            self._objects.append(object)
   
    def set_objects(self, list):
        self._objects = list(list)
       
    def get_objects(self):
        return self._objects
   
    def draw(self):
        for i, chat in enumerate(self._objects):
            chat.x = 5
            chat.y = 20 + i * 10
            pyxel.text(chat.x, chat.y, f"{chat.name} {chat.price}$", chat.color)


chat_list = [ShopObject("Jean-Louis", 1, 20)]

chat_shop = Shop(chat_list)


def catcreation (catlist, typee, x, y, m):
    taken = False
    if len(catlist) <= 6: 
        if (pyxel.frame_count % 900 == 0):
            catlist.append([random.randint(0, 120), random.randint(0, 120),typee, taken])
        elif m== True:
            catlist.append([x,y,typee, taken])
        return catlist
    return catlist
   
def catsdeplacement (catlist):
    global bitcoins
    if (pyxel.frame_count % 10 == 0):
        for cat in catlist:
            if cat[3] == False:
                if cat[1] > 120:
                    cat[1] -= 5
                elif cat[1] < 0:
                    cat[1] +=5
                else:
                    cat[1] += random.randint(-5, 5)
                 
                if cat[0] > 120:
                    cat[0] -= 5
                elif cat[0] < 0:
                    cat[0] +=5
                else:
                    cat[0] += random.randint(-5, 5)
            else:
                cat[0] = pyxel.mouse_x
                cat[1] = pyxel.mouse_y
            if (pyxel.frame_count % 100 == 0):
                for cat in catlist:
                    bitcoins += math.factorial(cat[2])
    return catlist

def cattouche():
    global catlist
    global maxcapacity
    """disparition du vaisseau et d'un cat si contact"""
    for cat in catlist:
        for touchedcat in catlist:
            if touchedcat == cat:
                continue
            if cat[2] == touchedcat[2]:
                if cat[0] <= touchedcat[0]+6 and cat[1] <= touchedcat[1]+6 and cat[0]+6 >= touchedcat[0] and cat[1]+6 >= touchedcat[1]:
                    catlist.remove(cat)
                    catlist.remove(touchedcat)
                    catcreation(catlist, cat[2]+1, cat[0],cat[1], True)
                    if cat[3] == True or touchedcat[3] == True:
                        maxcapacity = 0
                   
                   
def takecatwithmouse():
    global maxcapacity
    global catlist
    if maxcapacity == 0:
        for cat in catlist:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and \
                cat[0] <= pyxel.mouse_x <= cat[0] + 6 and \
                cat[1] <= pyxel.mouse_y <= cat[1] + 6:
                cat[3] = True
                maxcapacity = 1
    else:
        for cat in catlist:
            if cat[3] == True:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                    cat[3] = False
                    maxcapacity = 0
                   
           
           
# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global catlist
    global maxcapacity

    catlist = catcreation(catlist, 0,0,0, False)
    catlist = catsdeplacement(catlist)
    cattouche()
    takecatwithmouse()

    if pyxel.btnp(pyxel.KEY_S):
        chat_shop.is_displayed ^= True
       
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and \
       MENU_BTN_POS[0] <= pyxel.mouse_x <= MENU_BTN_POS[0] + MENU_BTN_SIZE[0] and \
       MENU_BTN_POS[1] <= pyxel.mouse_y <= MENU_BTN_POS[1] + MENU_BTN_SIZE[1]:
        chat_shop.is_displayed ^= True
   
    if chat_shop.is_displayed == True:
        for chat in chat_shop.get_objects():
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and \
               chat.x <= pyxel.mouse_x <= 118 and \
               chat.y <= pyxel.mouse_y <= chat.y + 5:               
                chat.bought = True
       
# =========================================================
# == DRAW
# =========================================================
def draw():
    global points, vies, bitcoins, catlist
    pyxel.cls(0)
    pyxel.text(50, 5, "Chat Jeu", 5)
   
    pyxel.text(5, 5, f"{bitcoins}$", 3)
   
    pyxel.rect(MENU_BTN_POS[0], MENU_BTN_POS[1], MENU_BTN_SIZE[0], MENU_BTN_SIZE[1], 12)

    if chat_shop.is_displayed:
        chat_shop.draw()
       
        for chat in chat_shop.get_objects():
            if chat.bought == True:
                if chat.price <= bitcoins:
                    if len(catlist) <= 6:
                        catcreation(catlist, 0, random.randint(0, 128), random.randint(0, 128), True)
                        bitcoins -= chat.price
                chat.bought = False
               
    for cat in catlist:
        pyxel.rect(cat[0], cat[1], 6, 6, cat[2]+1)
       
       
pyxel.run(update, draw)