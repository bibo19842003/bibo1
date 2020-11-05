import time
import re

# specify log file path
log_path = "my.log"

# open file and monitor newst line
number = 0
position = 0

with open(log_path, mode='r') as f:
    while True:
        line = f.readline().strip()
        if line:
            number += 1
            print("[number %s] %s" % (number, line))

            # TODO: check the kewword and do sth with line

        cur_position = f.tell() # record last time file read position

        if cur_position == position:
            time.sleep(10) # currently no line udpated, wait a while
            continue
        else:
            position = cur_position
