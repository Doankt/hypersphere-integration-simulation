import time
import monte as mte
import cubeintegration as cube
import assignment_tools as atools

# Required constants
RADIUS = 1
DIMENSION = 2
K_VALUE = 17000

# Optional constants
N_VALUE = None

if __name__ == "__main__":
    start = time.time()

    # ##############################################################
    # #################### Single Run Functions ####################
    # ##############################################################

    # print(mte.monte_integrate(RADIUS, DIMENSION, N_VALUE))
    # print(cube.cube_integrate(RADIUS, DIMENSION, K_VALUE))

    # ###################################################################################
    # #################### Absolute Run Functions (4 digit accuracy) ####################
    # ###################################################################################

    # print(mte.absolute_monte(RADIUS, DIMENSION))
    # print(cube.absolute_cube(RADIUS, DIMENSION, K_VALUE))

    # #############################################################
    # #################### Assignment Specific ####################
    # #############################################################

    num_samples = 1000000

    # print(atools.fixed_costs(RADIUS, DIMENSION, num_samples))
    # print(atools.most_accurate_value(RADIUS, DIMENSION, num_samples))

    # ################################################################
    # #################### Generate Multiple Runs ####################
    # ################################################################

    run_count = 5

    # atools.generate_monte_runs(RADIUS, DIMENSION, run_count)
    # atools.generate_cube_runs(RADIUS, DIMENSION, K_VALUE, run_count)

    print("Runtime:", time.time() - start)
