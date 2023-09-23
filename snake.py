import pygame as pg
import random

#color settings
background_clr = (0,0,0)
hud_clr = (0,0,100)
snake_clr = (255,255,255)
snakehead_clr = (255,0,0)
food_clr = (0,255,0)
lines_clr = (180,0,0)
text_clr = (255,255,255)
grid_clr = (100,100,100)

#logic settings
scale = 20
boardsize = (30,20)
max_fps = 100
move_speed = 6

#game settings
# the number of foods that should be on screen at the same time
max_foods = 4
# if the snake should teleport when running into a wall
woosh = True
# how many moves can be quequed in one move frame
max_move_queque = 3
# if the snake should be drawn as full squares
lq_snake = False
# if the game should draw ortogonal lines for each food
draw_crosshair = False
# if the game should draw a grid at each square
draw_grid = False
# if you should be invincible to all damage
godmode = False


#controls
controls = {
    "LEFT":[pg.K_a,pg.K_LEFT],
    "UP":[pg.K_w,pg.K_UP],
    "RIGHT":[pg.K_d,pg.K_RIGHT],
    "DOWN":[pg.K_s,pg.K_DOWN]
    }



pg.init()

displaysize = (scale*boardsize[0],scale*boardsize[1]+4*scale)
display = pg.display.set_mode(displaysize)
update_state = [0,round(max_fps/move_speed)]
font = pg.font.SysFont("Calibri",round(2*scale))
pg.display.set_caption("Snake")








class snake_segment:
    def __init__(self,pos,direc):
        self.x,self.y = pos
        self.pos = pos
        self.dirindex = direc
##        print(self.dirindex)



    def draw_self(self):
        if lq_snake:
            pg.draw.rect(display,snake_clr,(scale*self.x,scale*self.y,scale,scale))
        elif self.dirindex == 2:
            pg.draw.rect(display,snake_clr,(scale*self.x+scale*0.1, scale*self.y+scale*0.1, scale, scale*0.8))
        elif self.dirindex == 3:
            pg.draw.rect(display,snake_clr,(scale*self.x+scale*0.1, scale*self.y+scale*0.1, scale*0.8, scale))
        elif self.dirindex == 0:
            pg.draw.rect(display,snake_clr,(scale*self.x-scale*0.1, scale*self.y+scale*0.1, scale, scale*0.8))
        elif self.dirindex == 1:
            pg.draw.rect(display,snake_clr,(scale*self.x+scale*0.1, scale*self.y-scale*0.1, scale*0.8, scale))





class snake_class:
    def __init__(self):
        self.body = []
        self.headx,self.heady = [round(boardsize[0]/2),round(boardsize[1]/2)]
        self.direction = "NoneDir"







    def draw_self(self):

        for seg in self.body:
            seg.draw_self()



        if lq_snake or self.direction == "NoneDir":
            pg.draw.rect(display,snakehead_clr,(scale*self.headx,scale*self.heady,scale,scale))

        elif self.dirindex%2==0:
            pg.draw.rect(display,snakehead_clr,(scale*self.headx,scale*self.heady+scale*0.1,scale,scale*0.8))
        else:
            pg.draw.rect(display,snakehead_clr,(scale*self.headx+scale*0.1,scale*self.heady,scale*0.8,scale))


    def self_collisions(self):
        for seg in self.body:
            if seg.pos == [self.headx,self.heady]:
                    return True
        return False






    def move_self(self):
        global move_queque,foods,dead
        if len(move_queque) > 0:
            self.targetdir = move_queque.pop(0)
            self.dirindex = list(controls.keys()).index(self.targetdir)

            if self.dirindex%2==0 and self.direction not in ["LEFT","RIGHT"]: # even, so left-right
                self.direction = self.targetdir
            if self.dirindex%2!=0 and self.direction not in ["UP","DOWN"]: # even, so left-right
                self.direction = self.targetdir

        if self.direction != "NoneDir":
            self.body.append(snake_segment([self.headx,self.heady],self.dirindex))


        if self.direction == "LEFT":
            self.headx -= 1
        elif self.direction == "RIGHT":
            self.headx += 1
        elif self.direction == "UP":
            self.heady -= 1
        elif self.direction == "DOWN":
            self.heady += 1

        if woosh or godmode:
            if self.headx < 0:
                self.headx = boardsize[0]-1
            if self.headx > boardsize[0]-1:
                self.headx = 0


            if self.heady < 0:
                self.heady = boardsize[1]-1
            if self.heady > boardsize[1]-1:
                self.heady = 0
        else:
            if self.headx < 0:
                dead = True
            if self.headx > boardsize[0]-1:
                dead = True


            if self.heady < 0:
                dead = True
            if self.heady > boardsize[1]-1:
                dead = True





        eaten = False
        for food in foods:
            if [self.headx,self.heady] == food:
                foods.pop(foods.index(food))
                eaten = True


        if not eaten and self.direction != "NoneDir":
            self.body.pop(0)


        if self.self_collisions():
            if not godmode:
                dead = True



def draw_hud():
    pg.draw.rect(display,hud_clr,(0,boardsize[1]*scale,displaysize[0],4*scale))
    display.blit(font.render("SCORE: "+ str(len(snake.body)), False, text_clr), (scale, boardsize[1]*scale+scale))



def logic_calls():
    global update_state,foods
    if update_state[0] <= 0:
        snake.move_self()
        update_state[0] = update_state[1]
##        print(snake.headx,snake.heady)
##        print(foods)
    else:
       update_state[0] -= 1


    while len(foods) < max_foods:
        passed = False
        while not passed:
            passed = True
            fp = [random.randint(0,boardsize[0]-1),random.randint(0,boardsize[1]-1)]

            for sb in snake.body:
                if sb.pos == fp:
                    passed = False
                    break
            for fd in foods:
                if fp == fd:
                    passed = False
                    break
        foods.append(fp)





    clock.tick(max_fps)




def graphic_calls():
    display.fill(background_clr)

    if draw_grid:
        for i in range(boardsize[0]):
            pg.draw.line(display,grid_clr,(i*scale,0),(i*scale,displaysize[1]))
        for i in range(boardsize[1]):
            pg.draw.line(display,grid_clr,(0,i*scale),(displaysize[0],i*scale))





    if draw_crosshair:
        for food in foods:
            pg.draw.line(display,lines_clr,(food[0]*scale+scale/2,0),(food[0]*scale+scale/2,displaysize[1]),round(scale*0.1))
            pg.draw.line(display,lines_clr,(0,food[1]*scale+scale/2),(displaysize[0],food[1]*scale+scale/2),round(scale*0.1))




    for food in foods:
        pg.draw.rect(display,food_clr,(food[0]*scale+scale*0.1,food[1]*scale+scale*0.1,scale*0.8,scale*0.8))


    snake.draw_self()
    draw_hud()
    if not dead:
        pg.display.flip()





def main():
    global dead,move_queque,clock,snake,foods
    foods = []
    dead = False
    clock = pg.time.Clock()
    snake = snake_class()
    move_queque = []
    while not dead:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                dead = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    dead = True


                for item in controls.items():
                    if event.key in item[1]:
                        if len(move_queque) < max_move_queque:
                            move_queque.append(item[0])
                        break


        logic_calls()
        graphic_calls()




main()
pg.quit()
quit()
