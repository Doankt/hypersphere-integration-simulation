import time
import doankt_stats as dstats
import math
import multiprocessing as mp
from monte import monte_integrate
from cubeintegration import cube_integrate


def generate_monte_runs(radius, dimension, n):
    '''
    Generates n runs of single Monte Carlo methods and writes to
    m_out.txt

    :param radius:
    :param dimension:
    :param n: Number of runs
    :return: None
    '''

    with open("m_out.txt", "w") as file:
        for i in range(n):
            s_time = time.time()
            res = monte_integrate(radius, dimension)

            e_time = time.time() - s_time
            print(res, e_time)
            file.write(str(res) + "\t" + str(e_time) + "\n")


def generate_cube_runs(radius, dimension, k, n):
    '''
    Generates n runs of single Cube methods and writes to
    c_out.txt

    :param radius:
    :param dimension:
    :param k: Sections per dimension
    :param n: Number of runs
    :return: None
    '''

    with open("c_out.txt", "w") as file:
        for i in range(n):
            s_time = time.time()
            res = cube_integrate(radius, dimension, k)

            e_time = time.time() - s_time
            print(res, e_time)
            file.write(str(res) + "\t" + str(e_time) + "\n")


def fixed_costs(radius, dimension, samples):
    '''
    Runs both integration methods using the same CPU cost

    :param radius:
    :param dimension:
    :param samples: Number of samples to use
    :return: Absolute difference between runs
    '''

    k = math.ceil(math.pow(samples, 1/dimension))

    print("Running Monte Carlo")
    monte_res = monte_integrate(radius, dimension, samples)

    print("Running Deterministic")
    cube_interval = cube_integrate(radius, dimension, k)
    full = cube_interval[1] / math.pow(radius*2/k, dimension)
    all_in = cube_interval[0] / math.pow(radius*2/k, dimension)
    part_in = full - all_in
    cube_res = (all_in + (part_in/2))*math.pow(radius*2/k, dimension)

    return abs(monte_res - cube_res)


def most_accurate_value(radius, dimension, samples):
    '''
    Runs all samples of the Monte Carlo method and returns the most accurate possible value

    :param radius:
    :param dimension:
    :param samples: Number of runs to use
    :return: The highest accuracy interval
    '''

    if dimension == 1:
        return (2.0*radius,2.0*radius)

    pool = mp.Pool(processes=20)
    data = None

    batches = math.floor(samples / 20)

    for batch_num in range(batches):
        print("Starting Batch:", batch_num)

        stime = time.time()
        if not data:
            data = pool.starmap(monte_integrate, [(radius, dimension)] * 20)
        else:
            data.extend(pool.starmap(monte_integrate, [(radius, dimension)] * 20))
        print("Batch", batch_num, "time:", time.time() - stime)

        interval = dstats.generate_interval(data, 0.99)
        print("Batch", batch_num, "interval:", interval)

    print("Starting Mod Batch")
    data.extend(pool.starmap(monte_integrate, [(radius, dimension)] * (samples%20)))
    interval = dstats.generate_interval(data, 0.99)
    print("Mod Batch interval:", interval)

    return tuple(interval)
