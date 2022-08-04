

import time

print_debug = True
print_debug_level = 5

song_name = ""

def debug_print(string, dbg_lvl=1):
    if print_debug and (dbg_lvl <= print_debug_level):
        print("debug(lvl-"+ str(dbg_lvl) + "):"  + song_name +" ; "  + string)


def delaySec(seconds, msg=None, dbg_lvl=1):
    if msg is None:
        debug_print ("Delaying " + str(seconds) + " seconds..", dbg_lvl)
    else:
        debug_print (msg + " Delaying " + str(seconds) + " seconds..", dbg_lvl)
    time.sleep(seconds)
    debug_print (" - - - Delay Done!", 3)
