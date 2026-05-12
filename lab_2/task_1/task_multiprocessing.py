import multiprocessing
import time

N = 1_000_000_000
# N = 10000000000000
NUM_PROCESSES = 4


def calculate_sum(start, end):
    local_sum = 0

    for i in range(start, end + 1):
        local_sum += i

    return local_sum


if __name__ == "__main__":

    chunk_size = N // NUM_PROCESSES
    tasks = []

    for i in range(NUM_PROCESSES):

        start_num = i * chunk_size + 1

        if i == NUM_PROCESSES - 1:
            end_num = N
        else:
            end_num = (i + 1) * chunk_size

        tasks.append((start_num, end_num))
    print('start')

    start_time = time.time()

    with multiprocessing.Pool(NUM_PROCESSES) as pool:
        results = pool.starmap(calculate_sum, tasks)

    total_sum = sum(results)

    end_time = time.time()

    print("Multiprocessing:")
    print("Sum =", total_sum)
    print("Time =", end_time - start_time)


