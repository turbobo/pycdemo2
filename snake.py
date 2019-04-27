class Point:              #点由行列组成
    row=0
    col=0
    def __init__(self,row,col):
        self.row=row
        self.col=col

    def copy(self):           #复制自己
        return Point(row=self.row,col=self.col)

#初始化框架
import pygame
import random     #随机库
import sys
import time
from pygame.locals import *
from collections import deque

pygame.init()                                           #初始化背景音乐
pygame.mixer.init()
pygame.mixer.music.load("She.flac")                     # 加载音乐，MP3音乐文件放在代码文件所在文件夹中

if pygame.mixer.music.get_busy() == False:
    pygame.mixer.music.play()

#初始化
pygame.init()
W=800               #宽
H=600               #高

ROW=30              #6行，每行高100
COL=40              #8列，每列宽100

size=(W,H)
window=pygame.display.set_mode(size)
pygame.display.set_caption('贪吃蛇')        #设置标题
bg_color=(255,255,255)                      #背景色
snake_color=(200,200,200)                   #蛇身颜色
head=Point(row=int(ROW/2),col=int(COL/2))                  #蛇头
head_color=(99,184,255)

snakes=[                                                   #gen_food 函数会用到head,snake，所以它们要先定义
    Point(row=head.row,col=head.col+1),
    Point(row=head.row,col=head.col+3),
    Point(row=head.row,col=head.col+2),
]                               #初始化蛇身

#生成食物
def gen_food():
    while 1:        #可能会多次碰到
        pos=Point(row=random.randint(0,ROW-1),col=random.randint(0,COL-1))

        is_coll=False    #碰上is_coll
        #检测生成的食物是否跟蛇碰上
        if head.row==pos.row and head.col==pos.col:
            is_coll=True
            break

        # 遍历整个蛇身
        for snake in snakes:
            if snake.row==pos.row and snake.col==pos.col:
                is_coll=True

        if not is_coll:
            break                   #未碰撞，跳出循环

    return pos


#定义坐标
food=gen_food()                               #食物随机
food_color=(200,200,200)

direct='left'                                             #默认方向

#定义方块
def rect(point,color):
    cell_width=W/COL                                        #每列宽
    cell_height=H/ROW

    left=point.col*cell_width                               #每行高
    top=point.row*cell_height

    pygame.draw.rect(
     window,color,
        (left,top,cell_width,cell_height)
    )

    pass

#游戏循环
quit=True                                   #变量quit
# pause=True
clock=pygame.time.Clock()                   #clock游戏时间控制

while quit:
    #处理事件
    for event in pygame.event.get():        #用户输入的事件队列,用循环处理所有事件
        if event.type==pygame.QUIT:
            quit=False
        elif event.type==pygame.KEYDOWN:      #键盘输入
            # print(event)                      #打印键盘操作对应的key值
            if event.key==273 or event.key==119:              #上操作
                if direct=='left' or direct=='right':
                    direct='up'
            elif event.key==274 or event.key==115:
                if direct == 'left' or direct == 'right':
                    direct = 'down'
            elif event.key == 276 or event.key==97:
                if direct == 'up' or direct == 'down':
                    direct = 'left'
            elif event.key==275 or event.key==100:
                if direct == 'up' or direct == 'down':
                    direct = 'right'
            # elif event.key==32:                        #空格时暂停
            #     snakes=False
                # pause=False

    #吃东西 食物行列 和 头的行列重合
    eat=(head.row==food.row and head.col==food.col)

    #重新产生食物
    if eat:
        food=gen_food()

    #处理身子
    #1.把原来的头，插入到snakes的头上，从0第一个位置插入，不管吃没吃到，都前进一位
    snakes.insert(0,head.copy())

    #2.没吃到，把snakes的尾巴删掉，保持长度不变
    if not eat:
        snakes.pop()                      #snakes.pop()  移除尾巴

    #移动
    if direct=='left':
        head.col-=1
    elif direct=='right':
        head.col+=1
    elif direct=='up':
        head.row-=1
    elif direct=='down':
        head.row+=1

    #碰撞检测
    dead=False

    #1.撞墙
    if head.row<0 or head.col<0 or head.row>=ROW or head.col>=COL:
        dead=True

    #2.撞自己
    for snake in snakes:
        if head.row==snake.row and head.col==snake.col:                 #行列都相等
            dead=True
            break

    if dead:
        print("游戏结束")
        quit=False

    #渲染----画出来
    #背景\
    pygame.draw.rect(window,bg_color,(0,0,W,H))         #在哪个窗口上画方块，白色 从0，0开始 整个窗口

    #蛇头
    for snake in snakes:                                #蛇身是个列表
        rect(snake,snake_color)
    rect(head,head_color)
    rect(food,food_color)

    pygame.display.flip()          #让出控制权          # 刷新显示界面

    # 设置帧频
    clock.tick(10)  # 10帧  sleep(1000ms/10)

    # 收尾工作