from Mymqtt import Mymqtt
from receive import *
import pygame

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
car1 = pygame.image.load(car_image_name).convert_alpha()
car2 = pygame.image.load(car_image_name).convert_alpha()
car3 = pygame.image.load(car_image_name).convert_alpha()
# 小车初始参数
a = 0.061*ratio
# 必要信息：当前位置，当前速度，上一次运行时间,加速度,标志位（用于判断是否开始匀减速）,旋转角度，倒车标志位
list_value_car0 = [1*ratio, Coordinate_trans(0*ratio), 0, 0, 0, 1, 90, 0]
list_value_car1 = [1*ratio, Coordinate_trans(0*ratio), 0, 0, 0, 1, 90, 0]
list_value_car2 = [6.1*ratio, Coordinate_trans(0*ratio), 0, 0, 0, 1, 90, 0]
list_value_car3 = [6.1*ratio, Coordinate_trans(0*ratio), 0, 0, 0, 1, 90, 0]
list_value_car0[4] = a
list_value_car1[4] = a
list_value_car2[4] = a
list_value_car3[4] = a
# 油门档位分为1——10，标志位1代表前进，2代表后退，3代表急刹
# x,y,T,flag
# flag,1代表前进,2代表倒车,3代表急刹
list_init_car0 = [1*ratio, Coordinate_trans(0*ratio), 0, 1]
list_init_car1 = [1*ratio, Coordinate_trans(0*ratio), 0, 1]
list_init_car2 = [6.1*ratio, Coordinate_trans(0*ratio), 0, 1]
list_init_car3 = [6.1*ratio, Coordinate_trans(0*ratio), 0, 1]
# 初始化小车客户端
client_car0 = Mymqtt("car1")
client_car0.connect()
client_car1 = Mymqtt("car2")
client_car1.connect()
client_car2 = Mymqtt("car3")
client_car2.connect()
client_car3 = Mymqtt("car4")
client_car3.connect()

# 可以在这里由小车发布第一条数据
# 具体发送什么数据暂时没写
# client.push_info(position)
while True:
    # 循环20次，刷新一次屏幕
    if flash == 20:
        screen_show.fill((0, 0, 0))
        flash = 0
    else:
        flash = flash + 1

    # 获取数据
    car0_data = get_data(client_car0, list_value_car0)
    if car0_data:
        list_init_car0 = car0_data[0]
        list_value_car0 = car0_data[1]

    car1_data = get_data(client_car1, list_value_car1)
    if car1_data:
        list_init_car1 = car1_data[0]
        list_value_car1 = car1_data[1]

    car2_data = get_data(client_car2, list_value_car2)
    if car2_data:
        list_init_car2 = car2_data[0]
        list_value_car2 = car2_data[1]

    car3_data = get_data(client_car3, list_value_car3)
    if car3_data:
        list_init_car3 = car3_data[0]
        list_value_car3 = car3_data[1]
    # 运动
    list_value_car0 = car_straight(car0, screen_show, list_init_car0, list_value_car0)
    list_value_car1 = car_straight(car1, screen_show, list_init_car1, list_value_car1)
    list_value_car2 = car_straight(car2, screen_show, list_init_car2, list_value_car2)
    list_value_car3 = car_straight(car3, screen_show, list_init_car3, list_value_car3)

    # 发布数据
    client_list = [client_car0, client_car1, client_car2, client_car3]
    # client_list = [client_car0]
    value_list = [list_value_car0, list_value_car1, list_value_car2, list_value_car3]
    # value_list = [list_value_car0]
    publish_data(client_list, value_list)
