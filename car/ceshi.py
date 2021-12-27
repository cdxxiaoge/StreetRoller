from Mymqtt import Mymqtt
from receive import *
import pygame
# 位置、速度、加速度三个量都要记得进行模拟和现实的转化
# 屏幕刷新
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
    # 每来一组数据，刷新一遍队列
    if client_car0.data:
        data = invert(client_car0.data['pyload'])
        client_car0.data = None
        client_car0.queue.queue.clear()
        for i in data:
            client_car0.queue.put(i)
    #############################################
    # 更新目标位置信息
    if client_car0.queue.empty() is False:
        client_car0.IsRun = 1
        pos_time = client_car0.queue.get()
        for i in range(len(pos_time)):
            if i < 2:
                client_car0.target_pos[i] = pos_time[i] * client_car0.ratio
            else:
                t = pos_time[i]
        client_car0.last_runtime = time.time()
        client_car0.target_time = t - client_car0.last_runtime
    # 开始运动





