import threading
import time

N = 1_000_000_000
# N = 10000000000000
NUM_THREADS = 4

results = [0] * NUM_THREADS


def calculate_sum(start, end, index):
    local_sum = 0

    for i in range(start, end + 1):
        local_sum += i

    results[index] = local_sum


if __name__ == "__main__":
    chunk_size = N // NUM_THREADS
    threads = []
    start_time = time.time()

    for i in range(NUM_THREADS):
        start_num = i * chunk_size + 1

        if i == NUM_THREADS - 1:
            end_num = N
        else:
            end_num = (i + 1) * chunk_size

        thread = threading.Thread(
            target=calculate_sum,
            args=(start_num, end_num, i)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    total_sum = sum(results)

    end_time = time.time()

    print("Threading:")
    print("Sum =", total_sum)
    print("Time =", end_time - start_time)