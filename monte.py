import math
import random
import time
import multiprocessing as mp
import doankt_stats as dstats
from spacetools import distance

N_TABLE = {
    2:1000000,
    3:500000
}


def monte_integrate(radius, dimensions, cust_n_value = None):
    '''
    Generates random points in a hyper cube around a n-sphere

    :param radius:
    :param dimensions:
    :param cust_n_value: Custom n points generated
    :return: Volume of the n-sphere
    '''

    hits = 0
    miss = 0
    origin = [0]*dimensions

    if cust_n_value:
        n = cust_n_value
    elif dimensions in N_TABLE:
        n = N_TABLE[dimensions]
    else:
        n = 250000

    for i in range(n):

        point = []
        for _ in range(dimensions):
            point.append(random.uniform(-1, 1))
        if distance(point, origin) <= radius:
            hits += 1
        else:
            miss += 1

    return hits / (hits + miss) * math.pow(radius*2, dimensions)


def absolute_monte(radius, dimension):
    '''
    Runs monte_integrate until 4 digits of precision is reached

    :param radius:
    :param dimension:
    :return: Interval of the n-sphere to 4 digits of precision
    '''

    if dimension == 1:
        return (2.0*radius,2.0*radius)

    pool = mp.Pool(processes=20)
    data = None

    batch_num = 0
    while True:
        print("Starting Batch:", batch_num)

        stime = time.time()
        if not data:
            data = pool.starmap(monte_integrate, [(radius, dimension)] * 20)
        else:
            data.extend(pool.starmap(monte_integrate, [(radius, dimension)] * 20))
        print("Batch", batch_num, "time:", time.time() - stime)

        interval = dstats.generate_interval(data, 0.99)
        print("Batch", batch_num, "interval:", interval)

        if dstats.check_digit_match(interval[0], interval[1]) >= 4:
            break

        batch_num += 1

    return tuple(interval)
