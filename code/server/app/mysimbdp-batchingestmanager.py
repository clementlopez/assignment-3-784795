#!/usr/bin/python3

import time
import os
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def on_created(event):
    # print(f"hey, {event.src_path} has been created!")
    path = event.src_path.split('/')
    if os.path.exists(event.src_path):
        if (len(path) == 4) and (path[0] == ".") and (path[2] == "data"):
            file_size = os.path.getsize(event.src_path) / 1024
            nb_lines = int(os.popen('wc -l ' + event.src_path).read().split()[0])
            if nb_lines > 0:
                nb_lines = nb_lines - 1
            begin =  time.time()
            result = os.system("python ./"+path[1]+"/clientbatchingestapp.py -file "+os.getcwd()+"/"+path[1]+"/data/"+path[3])
            end =  time.time()
            if result == 0:
                logging.info("Ingestion of the file: %s for %s - size: %s KB - %s lines ingested in %s seconds" %(path[3], path[1], str(file_size), str(nb_lines), str(end-begin)))
            else:
                logging.debug("Ingestion Failed for the file: %s for %s - size: %s KB" %(path[3], path[1], str(file_size)))
        else:
            logging.info("Detection of a file creation that does not require a call to clientbatchingestapp")

if __name__ == "__main__":
    logging.basicConfig(filename='../server/batch_logs.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    patterns = "*"
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
    my_observer.join()

