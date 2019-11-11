from multiprocessing import Pool, TimeoutError, Process
import time
import os

def run_process(process):                                                             
    os.system('python {}'.format(process))

if __name__ == '__main__':
    #Multi-threads
    nbProcess = 10
    processes = []
    for i in range(nbProcess):
        processes.append('./fetchdata.py -u customer-1 -p password-1 --d client-input-dir'+str(i))
    for i in range(nbProcess):
        processes.append('./fetchdata.py -u customer-2 -p password-2 --d client-input-dir'+str(i))
    pool = Pool(processes=nbProcess*2)
    pool.map(run_process, processes)