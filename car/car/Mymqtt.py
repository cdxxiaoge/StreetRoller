import paho.mqtt.client as mqtt
import json 
import time
import collections


class Mymqtt(): 
    def __init__(self, name: str) -> None:

        self.NAME = name
        self.__HOSt = "127.0.0.1"
        self.__PORT = 1883
        self.__USER = "admin"
        self.__PASSWD = 'admin'

        # self.isConnected = False
        self.queue_trajectory = collections.deque()
        # self.queue_info = collections.deque()

    def on_connect(self, client, userdata, flags, rc): 
        '''
            连接后的回调函数
        '''
        pass 

    def on_subscribe(self, client, userdate, mid, granted_qos):
        '''
            订阅topic后的回调函数 
        '''
        pass 
    
    def on_message(self, client, userdata, msg): 
        '''
            收到订阅topic的消息后的回调函数
            # 在模拟器程序中只需要考虑收到的是预期轨迹的情况，因此简化了该部分代码, 可以根据控制器或车辆的需求重载
        '''
        data = {
            "topic": msg.topic, 
            "pyload": msg.payload
        }
        self.queue_trajectory.appendleft(data)

    def on_disconnect(self, client, userdata, rc):
        '''
            断开连接后的回调函数
        '''
        # self.isConnected = False
        pass

    def connect(self): 
        '''
            连接mqtt服务器，在连接时订阅自身的轨迹
        '''
        self.client = mqtt.Client(self.NAME) 
        self.client.username_pw_set(self.__USER, self.__PASSWD)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        try: 
            self.client.connect(self.__HOSt, self.__PORT)
            # self.isConnected = True
            self.client.loop_start()
            self.client.subscribe(self.NAME + "_trajectory", qos = 0)
        except:
            print("Connected Failed!")

    def subscribe(self, topics: list, Qoss: list): 
        '''
            手动增加订阅主题,适用于控制站，模拟器不需要
            params: 
                topics: 带订阅的主题列表 List[str]
                Qoss： 与topics中元素一一对应的qos列表 List[int]
        '''
        try: 
            for topic, qos in zip(topics, Qoss): 
                self.client.subscribe(topic, qos) 
        except: 
            print("Subscribe Error!")

    def push_info(self, position, speed, direction, isReversing): 
        '''
            推送自身信息
        '''
        data = self.payload_info_json(position, speed, direction, isReversing)
        try: 
            self.client.publish(self.NAME + "_info", payload=data, qos = 0)
        except:
            print("Publish Failed!")

    def push_info_json(self, data: json): 
        '''
            直接用json格式推送自身信息
        '''
        try: 
            self.client.publish(self.NAME + "_info", payload=data, qos = 0)
        except:
            print("Publish Failed!")

    def push_trajectory(self, target: str): 
        '''
            # 待完成
            向目标推送预期轨迹信息
            params: 
                target: 目标车辆名称
        '''
        pass 

    def push_trajectory_json(self, target: str, data: json): 
        '''
            直接以JSON格式向目标推送预期轨迹信息
            params: 
                target: 目标车辆名称
                data: json格式轨迹数据，详细格式参见self.payload_trajectory_json()
        '''
        try: 
            self.client.publish(str(target) + "_trajectory", payload=data, qos = 0)
        except:
            print("Publish Failed!")
        
    def disconnect(self): 
        try: 
            self.client.loop_stop()
            # self.isConnected = False
        except:
            print("Disconnected Failed!")
        
    def payload_info_json(self, position, speed, direction, isReversing) -> json: 
        '''
            创建JSON格式的车辆目前信息数据
            Params:
                type: payload类型，0为车辆信息，1为轨迹信息
                time：标准时间戳，发送自身信息时的时间 # 目前暂时假设所有车辆都是已对准的、标准的时间戳
                name: 车辆唯一标识
                position: 车辆目前位置
                speed: 车辆目前的行进速度
                direction：车辆目前的方向（也就是车头的朝向）
                isReversing: 标志位，表示当前车辆是否为倒车状态
        '''
        data = {
            "type": 0,
            "time": time.time(),
            "name": self.NAME,
            "position": position,
            "speed": speed,
            "direction": direction,
            "isReversing": isReversing
        }
        return json.dumps(data)
    
    def payload_trajectory_json(self, timeRange, targetPoints: json) -> json: 
        '''
            创建JSON格式的车辆目标轨迹信息数据
            Params:
                type: payload类型，0为车辆信息，1为轨迹信息
                time: 标准时间戳，地面站发送该轨迹时的时间，后续用于判断该指令是否已经过时
                name: 车辆唯一标识
                timeRange: 目标轨迹运行时间，表示这是接下来n 秒内的目标轨迹
                targetPoints: 轨迹集，格式如下
                {
                    {
                        timeID: 时间标识，1~n，表示这是接下来哪一秒的轨迹点
                        pointCount: 这一秒内目标点的数量，m
                        points: 位置点集，格式如下
                        {
                            {
                                targetPosition: 目标点位置
                                gear: 设定车辆行进时的挡位，目前是1~10档
                                isReversing: 标志位，表示是否需要车辆在倒车档下运行
                            }
                                        ……… # m个元素
                        }
                    }
                                ……… # n个元素
                }
        '''
        data = {
            "type": 1,
            "time": time.time(), 
            "name": self.NAME, 
            "timeRange": timeRange,
            "targetPoints": targetPoints
        }
        return json.dunmps(data)