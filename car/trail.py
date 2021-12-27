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
    data3 = []
    for i in range(len(data1)):
        data2.append(float(data1[i]))
        if (i+1) % 3 == 0:
            data3.append(data2)
            data2 = []
    return data3        # 返回列表


def pyexit():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.display.quit()
            exit()


# 获取小车目标速度
def getSpeed(client):
    if client.state == 2:
        # t*a1*a2+v0*a2
        x = client.target_message[1]*client.acceler_pos*client.acceler_ne+client.current_vel*client.acceler_ne
        # deta
        y = pow(client.target_message[1]*client.acceler_pos*client.acceler_ne, 2) +\
            2*client.target_message[1]*client.current_vel*client.acceler_pos*pow(
            client.acceler_ne, 2)-client.acceler_pos*client.acceler_ne*pow(
            client.current_vel, 2)-2*client.target_message[0]*(
            client.acceler_pos*pow(client.acceler_ne, 2)+client.acceler_ne*pow(client.acceler_pos, 2))
        if y > 0:
            client.target_vel = (x - sqrt(y))/(client.acceler_pos + client.acceler_ne)
        else:
            print("error")
    if client.state == 0:
        x = client.target_message[0] - pow(client.current_vel, 2)/client.acceler_ne/2
        y = client.target_message[1] - client.current_vel/client.acceler_ne
        client.target_vel = x / y


# 获取小车下一步运动状态
def getState(client):
    # 如果小车按照当前速度行驶，所能达到的最大距离
    s = client.current_vel*(client.target_message[1]-client.current_vel/client.acceler_ne)+pow(
        client.current_vel, 2)/client.acceler_ne/2
    # 进入它，说明小车保持匀速，最后减速到0即可
    if abs(s - client.target_message[0]) < 0.5:
        client.state = 1
        # 小车需要减速到0
        if pow(client.current_vel, 2)/client.acceler_ne/2 > client.target_message[0]:
            client.state = 0
    # 进入它，说明小车需要加速
    elif s < client.target_message[0]:
        client.state = 2
    else:
        client.state = 0


# 得到角度
def getAngle(client):
    if client.target_message[0] > 0.1:
        if client.target_pos[0] > client.current_pos[0]:
            client.angle = atan(abs(client.target_pos[1] - client.current_pos[1]) / (
                    client.target_pos[0] - client.current_pos[0])) / pi * 180
        elif abs(client.target_pos[1]-client.current_pos[1]) < 0.01 and client.target_pos[0] < client.current_pos[0]:
            client.angle = 180
        elif client.target_pos[0] < client.current_pos[0]:
            client.angle = 180 - atan(abs(client.target_pos[1] - client.current_pos[1]) / (
                    client.current_pos[0] - client.target_pos[0])) / pi * 180
        else:
            client.angle = 90
        if client.target_pos[1] > client.current_pos[1]:
            client.angle = 360 - client.angle


# 匀加速
def uniform_add(client, car, screen):
    # 目标距离
    current_time = time.time()
    time_lag = current_time-client.last_runtime
    client.last_runtime = current_time
    client.current_vel = client.current_vel + time_lag*client.acceler_pos
    client.sat()
    x = client.current_pos[0]
    y = client.current_pos[1]
    if client.target_pos[0] != x or client.target_pos[1] != y:
        x = x + time_lag * client.current_vel * (client.target_pos[0]-x) / sqrt(pow(client.target_pos[1] - y, 2) + pow(
            client.target_pos[0] - x, 2))
        y = y + time_lag * client.current_vel * (client.target_pos[1]-y) / sqrt(pow(client.target_pos[1] - y, 2) + pow(
            client.target_pos[0] - x, 2))
    client.current_pos = [x, y]
    client.target_message[0] = sqrt(pow(client.target_pos[1] - y, 2) + pow(client.target_pos[0] - x, 2))
    client.target_message[1] = client.target_message[1] - time_lag
    # 确定角度
    getAngle(client)
    pyexit()
    screen.blit(car, (x, y))
    pygame.display.update()


# 匀速运动
# list1=x,y,v,flag
# list2=x0,y0,speed,last_time,a,flag
def uniform(client, car, screen):
    # 目标距离
    current_time = time.time()
    time_lag = current_time - client.last_runtime
    client.last_runtime = current_time
    x = client.current_pos[0]
    y = client.current_pos[1]
    if client.target_pos[0] != x or client.target_pos[1] != y:
        x = x + time_lag * client.current_vel * (client.target_pos[0] - x) / sqrt(
            pow(client.target_pos[1] - y, 2) + pow(client.target_pos[0] - x, 2))
        y = y + time_lag * client.current_vel * (client.target_pos[1] - y) / sqrt(
            pow(client.target_pos[1] - y, 2) + pow(client.target_pos[0] - x, 2))
    client.current_pos = [x, y]
    client.target_message[0] = sqrt(pow(client.target_pos[1] - y, 2) + pow(client.target_pos[0] - x, 2))
    client.target_message[1] = client.target_message[1] - time_lag
    # 确定角度
    getAngle(client)
    pyexit()
    screen.blit(car, (x, y))
    pygame.display.update()


# 匀减速过程
# x,y,v,flag
# x0,y0,speed,last_time,a,flag
def uniform_sub(client, car, screen):
    # 目标距离
    current_time = time.time()
    time_lag = current_time - client.last_runtime
    client.last_runtime = current_time
    if client.current_vel > 0:
        client.current_vel = client.current_vel - time_lag * client.acceler_ne
        client.sat()
    x = client.current_pos[0]
    y = client.current_pos[1]
    if client.target_pos[0] != x or client.target_pos[1] != y:
        x = x + time_lag * client.current_vel * (client.target_pos[0] - x) / sqrt(
            pow(client.target_pos[1] - y, 2) + pow(client.target_pos[0] - x, 2))
        y = y + time_lag * client.current_vel * (client.target_pos[1] - y) / sqrt(
            pow(client.target_pos[1] - y, 2) + pow(client.target_pos[0] - x, 2))
    client.current_pos = [x, y]
    client.target_message[0] = sqrt(pow(client.target_pos[1] - y, 2) + pow(client.target_pos[0] - x, 2))
    client.target_message[1] = client.target_message[1] - time_lag
    # 确定角度
    getAngle(client)
    pyexit()
    screen.blit(car, (x, y))
    pygame.display.update()


def straight(client, car, screen):
    # 完全接近目标点
    if client.target_message[0] < 0.001:
        client.current_pos = client.target_pos
        client.IsRun = 0
        client.current_vel = 0
        client.backoff = 0
        client.state = 1
        print(time.time())
    # 匀减速
    if client.state == 0:
        uniform_sub(client, car, screen)
    # 匀速
    if client.state == 1:
        uniform(client, car, screen)
    # 匀加速
    if client.state == 2:
        uniform_add(client, car, screen)










