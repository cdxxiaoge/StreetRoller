import json
import paho.mqtt.client as mqtt
import time
from trail import Coordinate_trans


# 这个程序可以用来单独发送数据给小车，使小车动起来
# 如果和郭定的轨迹控制程序联调的话，这个程序就没用
def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# 600为keepalive的时间间隔
client.connect('127.0.0.1', 1883, 600)
current_time = time.time()
# 发送数据
re = [[1, 20, current_time + 30], [1, 0, current_time + 60], [6, 20, current_time + 100]]
re_json = json.dumps(re)
client.publish('car0_trajectory', payload=re_json, qos=0)
time.sleep(5)
# 再次发送
re = [[1, 25, current_time + 37], [1, 0, current_time + 67], [6, 20, current_time + 107]]
re_json = json.dumps(re)
client.publish('car0_trajectory', payload=re_json, qos=0)