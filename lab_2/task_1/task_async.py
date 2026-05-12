import asyncio
import time

N = 1_000_000_000
# N = 10000000000000
NUM_TASKS = 4


async def calculate_sum(start, end):
    local_sum = 0
    for i in range(start, end + 1):
        local_sum += i
    return local_sum    


async def main():

    chunk_size = N // NUM_TASKS
    tasks = []

    for i in range(NUM_TASKS):

        start_num = i * chunk_size + 1

        if i == NUM_TASKS - 1:
            end_num = N
        else:
            end_num = (i + 1) * chunk_size

        tasks.append(
            asyncio.create_task(
                calculate_sum(start_num, end_num)
            )
        )

    results = await asyncio.gather(*tasks)

    return sum(results)


start_time = time.time()

total_sum = asyncio.run(main())

end_time = time.time()

print("Asyncio:")
print("Sum =", total_sum)
print("Time =", end_time - start_time)