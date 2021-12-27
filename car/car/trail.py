from math import *
import pygame
import time
from pygame.locals import *
import json


def Coordinate_trans(y):
    # 600为生成的窗口的高度
    # 生成窗口screen_show = pygame.display.set_mode((1000, 600), 0, 32)
    #  只需转换y坐标，即可使得以左下角为坐标原点
    y = 600-y
    return y


# 将接收的字符串转化为列表
# 和郭定联调的时候用
# def invert(re):
#     # 此处固定油门值和方向 后续需要协商数据格式
#     data = json.loads(re)
#     # print(data)
#     flag = 1
#     if data['direction'] == 'backward':
#         flag = 2
#     data2 = [data['x'], data['y'], 9, flag]
#     return data2          # 返回列表

# 自己测试的时候用
def invert(data_addr):
    data = data_addr.decode()
    data = data.replace(",", " ")
    data = data.replace("[", " ")
    data = data.replace("]", " ")
    data1 = data.split()
    data2 = []
    for num in data1:
        data2.append(float(num))
    return data2          # 返回列表


def pyexit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            exit()


def uniform_add(list1, list2, car, screen):
    # 目标距离
    s = sqrt(pow(list1[1] - list2[1], 2) + pow(list1[0] - list2[0], 2))
    current_time = time.perf_counter()
    time_lag = current_time-list2[3]
    list2[3] = current_time
    list2[2] = list2[2] + time_lag*list2[4]
    x = list2[0]
    y = list2[1]
    if list1[1] != y or list1[0] != x:
        x = x + time_lag*list2[2] * (list1[0]-x) / sqrt(pow(list1[1] - y, 2) + pow(list1[0] - x, 2))
        y = y + time_lag*list2[2] * (list1[1]-y) / sqrt(pow(list1[1] - y, 2) + pow(list1[0] - x, 2))
    list2[0] = x
    list2[1] = y
    # 确定角度
    if s > 0.1:
        if list1[0] > list2[0]:
            list2[6] = atan(abs(list1[1] - list2[1]) / (list1[0] - list2[0])) / pi * 180
        elif abs(list1[1]-list2[1]) < 0.01 and list1[0] < list2[0]:
            list2[6] = 180
        elif list1[0] < list2[0]:
            list2[6] = 180 - atan(abs(list1[1] - list2[1]) / (list2[0] - list1[0])) / pi * 180
        else:
            list2[6] = 90
        if list1[1] > list2[1]:
            list2[6] = 360 - list2[6]
    pyexit()
    screen.blit(car, (x, y))
    pygame.display.update()
    return list2


# 匀速运动
# list1=x,y,v,flag
# list2=x0,y0,speed,last_time,a,flag
def uniform(list1, list2, car, screen):
    # 目标距离
    s = sqrt(pow(list1[1] - list2[1], 2) + pow(list1[0] - list2[0], 2))
    current_time = time.perf_counter()
    # 运行时间差
    time_lag = current_time - list2[3]
    list2[3] = current_time
    x = list2[0]
    y = list2[1]
    if list1[1] != y or list1[0] != x:
        x = x + time_lag*list2[2] * (list1[0]-x) / sqrt(pow(list1[1] - y, 2) + pow(list1[0] - x, 2))
        y = y + time_lag*list2[2] * (list1[1]-y) / sqrt(pow(list1[1] - y, 2) + pow(list1[0] - x, 2))
    list2[0] = x
    list2[1] = y
    # 确定角度
    if s > 0.1:
        if list1[0] > list2[0]:
            list2[6] = atan(abs(list1[1] - list2[1]) / (list1[0] - list2[0])) / pi * 180
        elif abs(list1[1]-list2[1]) < 0.01 and list1[0] < list2[0]:
            list2[6] = 180
        elif list1[0] < list2[0]:
            list2[6] = 180 - atan(abs(list1[1] - list2[1]) / (list2[0] - list1[0])) / pi * 180
        else:
            list2[6] = 90
        if list1[1] > list2[1]:
            list2[6] = 360 - list2[6]
    pyexit()
    screen.blit(car, (x, y))
    pygame.display.update()
    return list2


# 匀减速过程
# x,y,v,flag
# x0,y0,speed,last_time,a,flag
def uniform_sub(list1, list2, car, screen):
    # 目标距离
    s = sqrt(pow(list1[1] - list2[1], 2) + pow(list1[0] - list2[0], 2))
    current_time = time.perf_counter()
    time_lag = current_time - list2[3]
    list2[3] = current_time
    if list2[2] > 0:
        list2[2] = list2[2] - time_lag * list2[4]
    else:
        list2[5] = 2
        list2[2] = 0
    x = list2[0]
    y = list2[1]
    if list1[1] != y or list1[0] != x:
        x = x + time_lag*list2[2] * (list1[0]-x) / sqrt(pow(list1[1] - y, 2) + pow(list1[0] - x, 2))
        y = y + time_lag*list2[2] * (list1[1]-y) / sqrt(pow(list1[1] - y, 2) + pow(list1[0] - x, 2))
    list2[0] = x
    list2[1] = y
    # 确定角度
    if s > 0.1:
        if list1[0] > list2[0]:
            list2[6] = atan(abs(list1[1] - list2[1]) / (list1[0] - list2[0]))/pi*180
        elif abs(list1[1]-list2[1]) < 0.01 and list1[0] < list2[0]:
            list2[6] = 180
        elif list1[0] < list2[0]:
            list2[6] = 180-atan(abs(list1[1] - list2[1]) / (list2[0] - list1[0]))/pi*180
        else:
            list2[6] = 90
        if list1[1] > list2[1]:
            list2[6] = 360 - list2[6]
    pyexit()
    screen.blit(car, (x, y))
    pygame.display.update()
    return list2


# list1=x,y,v,flag
# list2=x0,y0,speed,last_time,a,flag

def straight(list1, list2, car, screen):
    # 目标距离
    s = sqrt(pow(list1[1] - list2[1], 2) + pow(list1[0] - list2[0], 2))
    # 急刹
    if list1[3] == 3:
        list2[2] == 0
        list2[3] == time.perf_counter()
        # 急刹结束后开始加速
        list2[5] == 1
        return list2

    if list2[2] == 0:
        # 更新当前时间
        list2[3] = time.perf_counter()

    if list2[5] == 0:
        list2 = uniform_sub(list1, list2, car, screen)
        # print("降速")
        return list2
    else:
        if (pow(list2[2], 2) / list2[4] / 2) > s:
            list2[5] = 0
        else:
            if abs(list1[2]-list2[2]) < 0.01 and list1[2] != 0:
                list2[2] = list1[2]
                # print("匀速")
                list2 = uniform(list1, list2, car, screen)
            elif list1[2] > list2[2] and list2[5] == 1:
                # print("匀加速")
                list2 = uniform_add(list1, list2, car, screen)
            elif list1[2] < list2[2]:
                list2[5] = 0
        return list2

