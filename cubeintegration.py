import math
import time
import doankt_stats as dstats
from itertools import product
from spacetools import distance


def generate_dimension_list(radius, k):
    '''
    Generates all sections for one dimension

    :param radius:
    :param k:
    :return: List of all point values needed in one dimension
    '''

    ret = []
    volume_per = 2*radius/k
    running_tot = -1*radius
    for i in range(k+1):
        ret.append(running_tot)
        running_tot += volume_per
    return ret


def generate_cubes(dimension_list, radius, dimensions, k):
    '''
    Generates all possible cubes needed to integrate

    :param dimension_list:
    :param radius:
    :param dimensions:
    :param k:
    :return: List of all n-cubes
    '''

    ret = []
    add_table = [x for x in product(range(2), repeat=dimensions)]
    origin = [0]*dimensions
    distance_dict = dict()

    for point in product(dimension_list, repeat=dimensions):
        if radius not in point:
            temp_list = []
            for logic_tuple in add_table:
                temp_point = list(point)
                for i in range(len(logic_tuple)):
                    temp_point[i] += logic_tuple[i]*2*radius / k
                    if tuple(temp_point) not in distance_dict:
                        distance_dict[tuple(temp_point)] = distance(temp_point, origin)
                temp_list.append(distance_dict[tuple(temp_point)] <= radius)
            ret.append(temp_list)

    return ret


def cube_integrate(radius, dimensions, k):
    '''
    Integrates the volume of a n-blob with cutoff sections

    :param radius:
    :param dimensions:
    :param k:
    :return: Lower and upper bounds of the interval
    '''

    dimension_list = generate_dimension_list(radius, k)

    add_table = [x for x in product(range(2), repeat=dimensions)]
    origin = [0]*dimensions

    all_in = 0
    all_out = 0
    part_in = 0

    for point in product(dimension_list, repeat=dimensions):
        if radius not in point:
            temp_checker = []

            for logic_tuple in add_table:
                temp_point = list(point)

                for i in range(len(logic_tuple)):
                    temp_point[i] += logic_tuple[i] * 2 * radius / k

                temp_checker.append(distance(temp_point, origin) <= radius)

            if temp_checker.count(False) == 0:
                all_in += 1
            elif temp_checker.count(True) == 0:
                all_out += 1
            else:
                part_in += 1

    lower_bound = all_in * math.pow(radius*2/k, dimensions)
    upper_bound = lower_bound + part_in*math.pow(radius*2/k, dimensions)

    return (lower_bound, upper_bound)


def absolute_cube(radius, dimension, start_k):
    '''
    Integrates the volume of a n-blob with 4 digits precision

    :param radius:
    :param dimension:
    :param start_k:
    :return: The interval with 4 digits precision
    '''

    if dimension == 1:
        return (2.0*radius,2.0*radius)

    k = start_k

    run_num = 0
    while True:

        print("Starting Run:", run_num, "with k:", k)

        stime = time.time()
        interval = cube_integrate(radius, dimension, k)
        print("Run", run_num, "time:", time.time() - stime)

        print("Run", run_num, "interval:", interval)

        if dstats.check_digit_match(interval[0], interval[1]) >= 4:
            break
        else:
            k = math.ceil(k * 1.33)

        run_num += 1

    return interval
