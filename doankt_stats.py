import numpy as np
from scipy import mean
from scipy.stats import sem, t
import math


def truncate(f, n):
    '''
    Cuts a digit to n digits

    :param f:
    :param n:
    :return: Cut number
    '''

    return math.floor(f * 10 ** n) / 10 ** n


def check_digit_match(check1, check2):
    '''
    Checks if both numbers agree to 4 decimal places

    :param check1:
    :param check2:
    :return: Number of digits that agree
    '''

    sc1 = format(truncate(check1,3), ".3f")
    sc2 = format(truncate(check2,3), ".3f")

    print(sc1, sc2)
    for i in range(len(sc1)):
        if sc1[i] != sc2[i] and sc1[i] != ".":
            return i - 1

    return 4


def generate_interval(datalist, conf_interval):
    '''
    Generates a confidence interval using Student's t distribution

    :param datalist:
    :param conf_interval: Requested probability
    :return: Interval
    '''

    datalist = 1.0 * np.array(datalist)
    n = len(datalist)
    m = mean(datalist)
    stderr = sem(datalist)

    diff_value = stderr * t.ppf((1 + conf_interval) / 2, n - 1)
    return [m - diff_value, m + diff_value]