import pandas as pd
from scipy.spatial.distance import euclidean


def cluster_points(traj: pd.DataFrame, dis_threshold: float, time_threshold: float, invalid_limits: int):
    """
    在规定时间及以上，某物体连续移动的距离没有超过聚类点的距离阈值，
    期间允许出现某几次阈值距离外的畸变点，那么这样的一些点统一可以聚类为一个点
    """
    new_trajectory = pd.DataFrame()
    x = [traj['x'].values[0]]
    y = [traj['y'].values[1]]
    t = [traj['timestamp'].values[0]]

    last_x = x[0]
    last_y = y[0]
    last_t = t[0]

    invalid_times = 0
    for i in range(1, len(traj)):
        cur_x = traj['x'].values[i]
        cur_y = traj['y'].values[i]
        cur_t = traj['timestamp'].values[i]
        if euclidean([cur_x, cur_y], [last_x, last_y]) >= dis_threshold or cur_t - last_t >= time_threshold:
            invalid_times += 1
            if invalid_times >= invalid_limits:
                last_x = cur_x
                last_y = cur_y
                invalid_times = 0
        x.append(last_x)
        y.append(last_y)
        t.append(last_t)
    new_trajectory['x'] = x
    new_trajectory['y'] = y
    new_trajectory['timestamp'] = t
    return new_trajectory
