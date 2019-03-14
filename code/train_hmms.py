import os
import subprocess
from multiprocessing import Pool


def run_job(n):
    FNULL = open(os.devnull, 'w')
    print("Started subprocess:      n_states = " + str(n))
    subprocess.call(['python', 'run_unsupervised.py', str(
        n), '1000'], stdout=FNULL, stderr=subprocess.STDOUT)
    print("Completed subprocess:    n_states = " + str(n))


if __name__ == '__main__':
    n_states = [1, 2, 4, 6, 8, 10, 12, 16, 20, 24, 32, 64]
    with Pool(processes=12) as pool:
        pool.map(run_job, n_states)
