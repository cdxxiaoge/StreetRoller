import time

from Mymqtt import Mymqtt
from receive import *
import pygame
# 位置、速度、加速度三个量都要记得进行模拟和现实的转化
flash = 0
# 背景图以及移动小车图
car_image_name = "car.png"
pygame.init()
# 生成窗口以及窗口标题
screen_show = pygame.display.set_mode((1000, 600), 0, 32)
pygame.display.set_caption("Little Case")
# 加载并转换图片
car0 = pygame.image.load(car_image_name).convert_alpha()
# 初始化小车客户端
client_car0 = Mymqtt("car0")
client_car0.connect()
while True:
    # 循环2次，刷新一次屏幕
    if flash == 2:
        screen_show.fill((0, 0, 0))
        flash = 0
    else:
        flash = flash + 1
    # 每来一组数据，刷新一遍队列
    PutData(client_car0)
    #############################################
    # 更新目标位置信息
    if client_car0.IsRun == 0 and client_car0.queue.empty() is False:
        client_car0.IsRun = 1
        # 刷新数据
        FlashData(client_car0)
        # 获取小车下一时刻运动状态
        getState(client_car0)
        # 获取小车目标速度
        getSpeed(client_car0)
        # 刷新最后运行时间
        client_car0.last_runtime = time.time()
        print(time.time())
    # 开始运动
    if client_car0.IsRun:
        # 获取小车下一时刻运动状态
        getState(client_car0)
        # 向目标点移动
        straight(client_car0, car0, screen_show)
        # 发送数据
        publish_data(client_car0)
