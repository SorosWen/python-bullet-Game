# Soros Wen
# Python Bullet Game
# Last Update: 2017 / 01 / 30
import threading
import random
import time
import math
from tkinter import *

class Isaac:
    def __init__(self, tk, game, element, item):
        self.game = game
        self.element = element
        self.item = item

        self.width = 1000
        self.height = 800
        self.canvas = Canvas(self.game, width = 1000, height = 800, bg = '#F4A460')
        self.canvas.pack()
        self.x = self.width / 2 
        self.y = self.height / 2
        self.r = 20
        self.Isaac = self.canvas.create_rectangle(self.x - self.r, self.y- self.r, self.x + self.r, self.y + self.r, fill = '#DC143C', outline = '#DC143C')

        self.whatever = open("HighestScore.txt", "r")
        self.highest = int(self.whatever.read())
        self.high = self.highest
        self.whatever.close()
		
        self.gameOver = True
        self.my_speed = 3.5
        self.attack = 10
        self.ball_time = 40
        self.balllist = []
        self.monsterlist = []
        self.balllist_delete = []
        self.j_list = []
        self.i_list = []
        self.recover = 0
        self.life = 200
        self.point = 0
        self.sleepTime = 0
        self.shield_value = 0
		
        self.Isaac_color = '#DC143C'
        self.full_life = "#000000"
        self.half_die = "#808080"
        self.shield_color = "#808080"
	
        self.start = Button(self.element, text = "Click To Start", fg = 'red', bg = 'orange', command = self.click_start)
        self.start.pack()

        self.Life = Label(self.item, text='Life:' + str(self.life), bg = 'orange', font = ('Helvetica', 19, 'bold'), compound = CENTER)
        self.Highest = Label(self.item, text='Highest Score:' + str(self.highest), bg = 'orange', font = ('Helvetica', 19, 'bold'))
        self.points = Label(self.item, text='Score:' + str(self.point), bg = 'orange', font = ('Helvetica', 19, 'bold'))    
        self.Life.grid(row = 0, column = 0, sticky = W)
        self.Highest.grid(row = 1, column = 0, sticky = W)
        self.points.grid(row = 2, column = 0, sticky = W)

        self.addx = False
        self.addy = False
        self.subtractx = False
        self.subtracty = False

        self.ballleft = False
        self.ballup = False
        self.ballright = False
        self.balldown = False

        self.ball_check = [0, 0, 0, 0]

        self.detect_key_press() 
        self.detect_key_press() 

        self.whatever1 = open("HighestScore.txt", "w")
        if self.point > self.high:
            self.whatever1.write(str(self.point))
        elif self.point <= self.high: 
            self.whatever1.write(str(self.high))
        self.whatever1.close()
    
    def detect_key_press(self):
        """ detect key press and adjust the direction of avatar and boolet accordingly. 
        """
        # avatar control
        self.canvas.bind_all('<KeyPress-Left>', self.addx1)
        self.canvas.bind_all('<KeyPress-Up>', self.addy1)
        self.canvas.bind_all('<KeyPress-Right>', self.subtractx1)
        self.canvas.bind_all('<KeyPress-Down>', self.subtracty1)
        
        self.canvas.bind_all('<KeyRelease-Left>', self.addx2)
        self.canvas.bind_all('<KeyRelease-Up>', self.addy2)
        self.canvas.bind_all('<KeyRelease-Right>', self.subtractx2)
        self.canvas.bind_all('<KeyRelease-Down>', self.subtracty2)

        # shield control
        self.canvas.bind_all('<KeyPress-e>', self.shield)

        # boolet control
        self.canvas.bind_all('<KeyPress-a>', self.ballleft_on)
        self.canvas.bind_all('<KeyPress-w>', self.ballup_on)
        self.canvas.bind_all('<KeyPress-d>', self.ballright_on)
        self.canvas.bind_all('<KeyPress-s>', self.balldown_on)

#        self.canvas.bind_all('<KeyRelease-a>', self.ballleft_off)
#        self.canvas.bind_all('<KeyRelease-w>', self.ballup_off)
#        self.canvas.bind_all('<KeyRelease-d>', self.ballright_off)
#        self.canvas.bind_all('<KeyRelease-s>', self.balldown_off)
		
    def click_start(self):
        self.gameOver = False
        self.createMonster()
        self.animate()

    def createMonster(self):
        for i in range(10):
            r = random.randint(1, 3)
            if r == 1:
                self.normalMonster()
            elif r == 2:
                self.hardMonster()
            elif r == 3:
                self.fastMonster()

    def normalMonster(self):
        self.x1 = random.randint(50, self.width - 50)
        self.y1 = random.randint(50, self.height - 50)
        self.r1 = 10
        self.speed = (random.randint(20, 25)) / 10
        self.score = 30
        self.color = "#FFFF00"
        self.monster_life = 30
        self.monster_factory(self.x1, self.y1, self.r1, self.speed, self.score, self.color, self.monster_life)

    def hardMonster(self):
        self.x2 = random.randint(50, self.width - 50)
        self.y2 = random.randint(50, self.height - 50)
        self.r2 = 10
        self.speed = (random.randint(15, 20)) / 10
        self.score = 10
        self.color = "#6B8E23"
        self.monster_life = 60
        self.monster_factory(self.x2, self.y2, self.r2, self.speed, self.score, self.color, self.monster_life)

    def fastMonster(self):
        self.x3 = random.randint(50, self.width - 50)
        self.y3 = random.randint(50, self.height - 50)
        self.r3 = 5
        self.speed = (random.randint(25, 30)) / 10
        self.score = 40
        self.color = "#00FFFF"
        self.monster_life = 10
        self.monster_factory(self.x3, self.y3, self.r3, self.speed, self.score, self.color, self.monster_life)

    def monster_factory(self, x, y, r, speed, score, color, life):
        self.canvas.create_rectangle(x - r, y - r, x + r, y + r, fill = color, outline = color, tag = "monster")
        self.monsterlist.append([x, y, r, color, speed, score, life, life])

    def animate(self):
        while not self.gameOver:
            if self.life <= 200:
                self.recover += 1
                
            if self.recover % 100 == 0 and self.life < 200:
                self.life += 1
                
            if self.point > self.highest:
                self.highest = self.point

            self.canvas.after(self.sleepTime)
            self.canvas.update() 
            self.canvas.delete(self.Isaac)
            self.canvas.delete("monster") 
            self.canvas.delete("ball")

            self.Life['text']= 'Life:' + str(self.life)
            self.Highest['text'] ='Highest Score:' + str(self.highest)
            self.points['text'] ='Score:' + str(self.point)
            
            self.show_Isaac()
			
            self.disappear()
            
            self.show_monster()
            
            for i in range (len(self.balllist)):
                self.canvas.create_oval(self.balllist[i][2] + 2, self.balllist[i][3] + 2, self.balllist[i][2] - 2, self.balllist[i][3] - 2, fill = self.balllist[i][4], outline = self.balllist[i][4], tag = "ball")
                self.balllist[i][2] += self.balllist[i][0]
                self.balllist[i][3] += self.balllist[i][1]
                self.balllist[i][5] -= 1
                if self.balllist[i][5] == 0:
                    self.balllist_delete.append(i)
            for num in range(len(self.balllist_delete) -1, -1, -1):
                self.balllist.pop(self.balllist_delete[num])
                self.balllist_delete.pop(num)

            self.move_operation()
            
            self.shoot()
			
    def show_Isaac(self):
        self.Isaac = self.canvas.create_rectangle(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = self.Isaac_color, outline = self.shield_color, width = self.shield_value / 10)

    def shield(self, evt):
        self.shield_value = 100

    def show_monster(self):
        for i in range (len(self.monsterlist)):
            self.stop(i)
            self.dx = ((self.monsterlist[i][4] * (self.x - self.monsterlist[i][0])) / (((self.x - self.monsterlist[i][0]) ** 2 + (self.y - self.monsterlist[i][1]) ** 2) ** 0.5))
            self.dy = ((self.monsterlist[i][4] * (self.y - self.monsterlist[i][1])) / (((self.x - self.monsterlist[i][0]) ** 2 + (self.y - self.monsterlist[i][1]) ** 2) ** 0.5))
            self.monsterlist[i][0] += self.dx
            self.monsterlist[i][1] += self.dy

            self.color_store = None
            if self.monsterlist[i][7] * 2 / 3 < self.monsterlist[i][6] <= self.monsterlist[i][7]:
                self.color_store = self.full_life
            elif self.monsterlist[i][7] / 3 < self.monsterlist[i][6] <= self.monsterlist[i][7] * 2 / 3:
                self.color_store = self.half_die
            elif self.monsterlist[i][6] <= self.monsterlist[i][7] / 3:
                self.color_store = self.monsterlist[i][3]
				
            self.canvas.create_rectangle(self.monsterlist[i][0] - self.monsterlist[i][2] + self.dx, self.monsterlist[i][1]- self.monsterlist[i][2] + self.dy, self.monsterlist[i][0] + self.monsterlist[i][2] + self.dx, self.monsterlist[i][1] + self.monsterlist[i][2] + self.dy, fill = self.monsterlist[i][3], outline = self.color_store, tag = "monster", width = 2)

    def disappear(self):
        for i in range (len(self.monsterlist)):
            for j in range(len(self.balllist)):
                if (((self.balllist[j][2] + 2 < self.monsterlist[i][0] + self.monsterlist[i][2]) and (self.balllist[j][2] + 2 > self.monsterlist[i][0] - self.monsterlist[i][2])) or ((self.balllist[j][2] - 2 < self.monsterlist[i][0] + self.monsterlist[i][2]) and (self.balllist[j][2] - 2 > self.monsterlist[i][0] - self.monsterlist[i][2]))) and (((self.balllist[j][3] + 2 < self.monsterlist[i][1] + self.monsterlist[i][2]) and (self.balllist[j][3] + 2 > self.monsterlist[i][1] - self.monsterlist[i][2])) or ((self.balllist[j][3] - 2 < self.monsterlist[i][1] + self.monsterlist[i][2]) and (self.balllist[j][3] - 2 > self.monsterlist[i][1] - self.monsterlist[i][2]))):
                    self.monsterlist[i][6] -= self.attack
                    if self.monsterlist[i][6] <= 0:
                        self.i_list.append(i)
                    self.j_list.append(j)
        self.j_list.sort()
        self.i_list.sort()
        for check in range(len(self.j_list) -1, -1, -1):
            if self.j_list[check] == self.j_list[check - 1] and check != 0:
                self.j_list.pop(check)
        for check in range(len(self.i_list) -1, -1, -1):
            if self.i_list[check] == self.i_list[check - 1] and check != 0:
                self.i_list.pop(check)

        for q in range(len(self.j_list) -1, -1, -1):
            self.balllist.pop(self.j_list[q])
        self.j_list = []
        
        for w in range(len(self.i_list) -1, -1, -1):
            self.point += self.monsterlist[self.i_list[w]][5]
            self.monsterlist.pop(self.i_list[w])
            if len(self.monsterlist) == 0:
                self.createMonster()
        self.i_list = []

    def stop(self, i):
        if (((self.monsterlist[i][0] + self.monsterlist[i][2] < self.x + self.r) \
            and (self.monsterlist[i][0] + self.monsterlist[i][2] > self.x - self.r)) or ((self.monsterlist[i][0] - self.monsterlist[i][2] < self.x + self.r) \
            and (self.monsterlist[i][0] - self.monsterlist[i][2] > self.x - self.r))) \
            and (((self.monsterlist[i][1] + self.monsterlist[i][2] < self.y + self.r) \
            and (self.monsterlist[i][1] + self.monsterlist[i][2] > self.y - self.r)) or ((self.monsterlist[i][1] - self.monsterlist[i][2] < self.y + self.r) \
            and (self.monsterlist[i][1] - self.monsterlist[i][2] > self.y - self.r))):

            if self.shield_value > 0:
                self.shield_value -= 1
            elif self.shield_value == 0:
                self.life -= 1
                
            if self.life == 0:
                self.gameOver = True
                self.Life['text']= 'Life:' + str(self.life)
                print ("Your score is: " + str(self.point))

    def move_operation(self):
        if self.x > 2 * self.r and self.addx == True:
            self.x -= self.my_speed
    
        if self.y > 2 * self.r and self.addy == True:
            self.y -= self.my_speed

        if self.x < self.width - 2 * self.r and self.subtractx == True:
            self.x += self.my_speed

        if self.y < self.height - 2 * self.r and self.subtracty == True:
            self.y += self.my_speed

    def addx1(self, evt):
        self.addx = True
    def addy1(self, evt):
        self.addy = True
    def subtractx1(self, evt):
        self.subtractx = True
    def subtracty1(self, evt):
        self.subtracty = True
		
    def addx2(self, evt):
        self.addx = False
    def addy2(self, evt):
        self.addy = False
    def subtractx2(self, evt):
        self.subtractx = False
    def subtracty2(self, evt):
        self.subtracty = False
		

    def ballleft_on(self, evt):
        self.ballleft = True
        for i in range(len(self.ball_check)):
            if self.ball_check[i] > 0:
                self.ball_check[i] += 1
        self.ball_check[1] += 1

    def ballleft_off(self, evt):
        self.ballleft = False
        for i in range(len(self.ball_check)):
            if self.ball_check[i] > 0:
                self.ball_check[i] -= 1
        self.ball_check[1] = 0

    def ballright_on(self, evt):
        self.ballright = True
        for i in range(len(self.ball_check)):
            if self.ball_check[i] > 0:
                self.ball_check[i] += 1
        self.ball_check[2] += 1
		
    def ballright_off(self, evt):
        self.ballright = False
        for i in range(len(self.ball_check)):
            if self.ball_check[i] > 0:
                self.ball_check[i] -= 1
        self.ball_check[2] = 0

    def balldown_on(self, evt):
        self.balldown = True
        for i in range(len(self.ball_check)):
            if self.ball_check[i] > 0:
                self.ball_check[i] += 1
        self.ball_check[3] += 1

    def balldown_off(self, evt):
        self.balldown = False
        for i in range(len(self.ball_check)):
            if self.ball_check[i] > 0:
                self.ball_check[i] -= 1
        self.ball_check[3] = 0

    def ballup_on(self, evt):
        self.ballup = True
        for i in range(len(self.ball_check)):
            if self.ball_check[i] > 0:
                self.ball_check[i] += 1
        self.ball_check[0] += 1

    def ballup_off(self, evt):
        self.ballup = False
        for i in range(len(self.ball_check)):
            if self.ball_check[i] > 0:
                self.ball_check[i] -= 1
        self.ball_check[0] = 0


    def shoot(self):
        check = 100
        check_name = 5
        for i in range(len(self.ball_check)):
            if self.ball_check[i] < check and self.ball_check[i] != 0:
                check = self.ball_check[i]
                check_name = i
        if check_name == 0:
            self.ballup_start()
        if check_name == 1:
            self.ballleft_start()
        if check_name == 2:
            self.ballright_start()
        if check_name == 3:
            self.balldown_start()

    def ballup_start(self):
        if self.ballup == True:
            self.movex = 0
            self.movey = -10
            self.radius = 10
            self.ball_color = '#DC143C'
            self.ball_factory(self.movex, self.movey, self.radius, self.ball_color)

    def ballleft_start(self):
        if self.ballleft == True:
            self.movex = -10
            self.movey = 0
            self.radius = 10
            self.ball_color = '#DC143C'
            self.ball_factory(self.movex, self.movey, self.radius, self.ball_color)

    def ballright_start(self):
        if self.ballright == True:
            self.movex = 10
            self.movey = 0
            self.radius = 10
            self.ball_color = '#DC143C'
            self.ball_factory(self.movex, self.movey, self.radius, self.ball_color)

    def balldown_start(self):
        if self.balldown == True:
            self.movex = 0
            self.movey = 10
            self.radius = 10
            self.ball_color = '#DC143C'
            self.ball_factory(self.movex, self.movey, self.radius, self.ball_color)

    def ball_factory(self, x, y, r, color):
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill = color, outline = color, tags = "ball")
        self.balllist.append([x, y, self.x, self.y, color, self.ball_time])


def main():
    tk = Tk()
    tk.title("The Binding of Isaac")

    game = Frame(tk, bd = 6, width = 1002, height = 802, relief = SUNKEN)
    game.grid_propagate(0)
    game.grid(row = 0, rowspan = 2, column = 1)

    element = Frame(tk, bd = 6, width = 200, height = 190, relief = SUNKEN)
    element.pack_propagate(0)
    element.grid(row = 0, column = 0)

    item = Frame(tk, bd = 6, width = 200, height = 602, relief = SUNKEN, bg = 'orange')
    item.grid_propagate(0)
    item.grid(row = 1, column = 0)

    isaac = Isaac(tk, game, element, item)
    tk.mainloop()

main()