#https://www.youtube.com/watch?v=IEEhzQoKtQU&ab_channel=CoreySchafer
import multiprocessing
import time

start = time.perf_counter()

def do_something(seconds):
    print(f'Sleeping {seconds} second...')
    time.sleep(seconds)
    print("Done sleeping")

processes = []

seconds = 1.5

for _ in range(10):
    p = multiprocessing.Process(target=do_something, args=[seconds])   
    p.start()
    processes.append(p)

for process in processes:
    process.join()


finish = time.perf_counter()
         
print(f'Finished in {round(finish-start, 2)} second(s)')
