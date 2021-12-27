import time
import math
import sys
import numpy as np
import PX4MavCtrlV4 as PX4MavCtrl

import json
import collections
import paho.mqtt.client as mqtt 

message_queue = collections.deque()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic, ' ++ ', msg.payload)
    topic = msg.topic 
    car_id = int(str(topic).split('_')[0].split('car')[-1])
    message = json.loads(msg.payload)
    posittion = message['position'] + [-1]
    direction = message['direction']
    isReversing = bool(message['isReversing'])
    message_queue.appendleft([car_id, posittion, direction, isReversing])

client = mqtt.Client("RflySim")
client.username_pw_set("admin", 'admin')
client.on_connect = on_connect
client.on_message = on_message
client.connect('127.0.0.1', 1883, 60)
client.loop_start()
# client.subscribe([("car1_info", 0), ("car2_info", 0), ("car3_info", 0), ("car4_info", 0)])

mav = PX4MavCtrl.PX4MavCtrler(20100)
mav.sendUE4Cmd(b'RflyChangeMapbyName OldFactory')    
time.sleep(2) 

# 字典，第一个元素为carID, 第二个元素为车辆类型， 51为钢轮, 1051为胶轮, 2051为摊铺机
# 注意，此处车辆的数量一定要与car_list中的相吻合
car_type = {
    1 : 51, 
    2 : 1051, 
    3 : 51, 
    4 : 1051
}

# 设置第一赛道车辆在地图中的的初始位置, 只与RflySim使用的坐标中马路所在位置有关, 改变这个值即改变第一辆车的位置
init_pos = [14,-119,-1] 

# 每个赛道之间的间距, 如果在控制程序"pathPlanning"中进行了更改，此处也要同步修改
line_space = 7.8 

# 同赛道之间每台车之间的间距
car_space = 5 

"""
元组, 车辆分布, (2,2)代表车辆分布为两行两列
|             |
|             |
|* --A--*     |
|       |     |  
|       B     |
|       |     |
|*      *     |

A为line_space, B为car_space
"""
car_list = (2, 2)

car_ids = [int(i) for i in range(car_list[0] * car_list[1], 0, -1)]
assert len(car_ids) == len(car_type), "len(car_list) != len(car_type)"

for i in car_ids: 
    client.subscribe("car" + str(i) + "_info", 0)

for i in range(car_list[0]):
    for j in range(car_list[1]): 
        pos_cal = [init_pos[0] - j * car_space, init_pos[1] + i * line_space, init_pos[2]]
        car_id = car_ids.pop()
        mav.sendUE4Pos2Ground(car_id, car_type[car_id], 0, pos_cal, np.zeros(3))
        time.sleep(0.1)

mav.sendUE4PosScale(100,152,0,[19,-130,-10],[0,0,math.pi * (1 / 2)],[0.01,0.01,0.01],0)
time.sleep(0.1)
mav.sendUE4Cmd(b'RflyChangeViewKeyCmd B 2')
time.sleep(0.1)
mav.sendUE4Cmd(b'RflyChangeViewKeyCmd S')

while True: 
    if len(message_queue) == 0: 
        time.sleep(0.1)
        continue
    message = message_queue.pop()
    print(message)
    message[1] = [message[1][1], message[1][0], message[1][2]]
    pos = np.asarray(message[1]) + np.asarray(init_pos) # 坐标系的转换
    # 如果倒车的话，将direction的方向调转180°即为当前车头对应的的方向
    if message[3]: 
        message[2] += 180.0
    angEuler = [0, 0, -(message[2] - 90) / 180 * math.pi]
    mav.sendUE4Pos2Ground(message[0], car_type[message[0]], 0, pos, angEuler)