import math


def absolute_volume(radius, dimensions):
    '''
    Returns the correct volume of a n-sphere

    :param radius:
    :param dimensions:
    :return: Volume of n-sphere
    '''

    return (math.pow(math.pi, dimensions/2)) / (math.gamma((dimensions/2) + 1)) * math.pow(radius, dimensions)


def distance(point_a, point_b):
    '''
    Calculates euclidean distance

    :param point_a:
    :param point_b:
    :return: Distance
    '''

    assert(len(point_a) == len(point_b))
    total = 0
    for i in range(len(point_a)):
        total += math.pow(point_a[i] - point_b[i], 2)
    return math.sqrt(total)
