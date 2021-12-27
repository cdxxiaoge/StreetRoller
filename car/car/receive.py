from trail import *

# 模拟和现实的换算比例
ratio = 5
# 油门档位分为1——10对应的速度
acceler = [0.56, 0.621, 0.682, 0.743, 0.804, 0.865, 0.926, 0.987, 1.048, 1.11]
# 设定小车加速度


def time_required(f):
    last = [time.time()]

    def decorator(*args, **kwargs):
        if time.time() - last[0] > 0.5:
            last[0] = time.time()
            return f(*args, **kwargs)
        else:
            pass
    return decorator


# 小车运动
def car_straight(car, screen, list_init, list_value):
    if list_init:
        # print("正在向目标点({}, {})移动".format(list_init[0], list_init[1]))
        list_value = straight(list_init, list_value, car, screen)
        return list_value


# 实时接收轨迹数据
def get_data(client, list_value):
    if client.queue_trajectory:
        list_init = client.queue_trajectory.pop()
        list_init = invert(list_init["pyload"])
        # 要进行现实和模拟的变换
        list_init[0] = list_init[0]*ratio
        list_init[1] = Coordinate_trans(list_init[1]*ratio)
        list_init[3] = int(list_init[3])
        # 将油门转化为速度,在小车模拟中50个像素点距离相当于1米
        list_init[2] = acceler[int(list_init[2]) - 1] * ratio
        list_value[5] = 1  # 接收到数据后防止车辆立刻减速
        if list_init[3] == 2:
            list_value[7] = 1
        else:
            list_value[7] = 0
        print(list_init)
        return (list_init, list_value)
    else:
        return None


# 发布轨迹信息
@time_required
def publish_data(client_list, value_list):
    # 每0.5秒发送一次
    for i in range(len(value_list)):
        position = [0, 0]
        position[0] = value_list[i][0] / ratio
        position[1] = Coordinate_trans(value_list[i][1]) / ratio
        speed = value_list[i][2] / ratio
        direction = value_list[i][6]
        isReversing = value_list[i][7]
        print([position,speed,direction])
        client_list[i].push_info(position, speed, direction, isReversing)