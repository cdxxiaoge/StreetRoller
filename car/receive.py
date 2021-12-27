from trail import *


def time_required(f):
    last = [time.time()]

    def decorator(*args, **kwargs):
        if time.time() - last[0] > 0.5:
            last[0] = time.time()
            return f(*args, **kwargs)
        else:
            pass
    return decorator


# 获取新数据后放入队列
def PutData(client):
    if client.data:
        client.IsRun = 0
        data = invert(client.data['pyload'])
        client.data = None
        client.queue.queue.clear()
        for i in data:
            client.queue.put(i)


# 从队列中获取数据后，刷新数据
def FlashData(client):
    pos_data = client.queue.get()
    for i in range(len(pos_data)):
        if i == 0:
            client.target_pos[i] = pos_data[i] * client.ratio
        if i == 1:
            client.target_pos[i] = Coordinate_trans(pos_data[i] * client.ratio)
        if i == 2:
            t = pos_data[i]
    # 更新目标距离等信息
    client.target_message[0] = sqrt(pow(client.target_pos[0] - client.current_pos[0], 2) +
                                         pow(client.target_pos[1] - client.current_pos[1], 2))
    client.target_message[1] = t - time.time()
    # 是否倒车
    if client.target_pos[1] > client.current_pos[1]:
        client.backoff = 1


# 发布轨迹信息
@time_required
def publish_data(client):
    # 每0.5秒发送一次
    position = [0, 0]
    position[0] = client.current_pos[0] / client.ratio
    position[1] = Coordinate_trans(client.current_pos[1]) / client.ratio
    speed = client.current_vel / client.ratio
    direction = client.angle
    isReversing = client.backoff
    print([position, speed, direction])
    client.push_info(position, speed, direction, isReversing)
