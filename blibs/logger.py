__author__ = 'biagio'

import os
import pprint
pp = pprint.PrettyPrinter(indent=4)
import inspect
import ntpath
from . import timestamps
import sys

def wlog(*args, **kwargs): # takes args and kwargs so that hte function can be overloaded
    # log_fh, log_fn, log_fp, msg_details, details, msg, type
    ts = timestamps.get_ts() #needs timestamps libs
    #print "ts: ", ts #debug
    #print "args :", args #debug
    if (len(args) == 0):
        if 'fh' not in kwargs:
            cwd = os.getcwd() # get the current working directory
            log_dir = cwd + os.sep + "log"
            frm = inspect.stack()[1]
            if (os.path.isdir(log_dir)):
                print("log dir is real: ", log_dir)
            else:
                print("log dir no good: ", log_dir)
            log_name = get_call_script_name()
            log_name += "_log.txt"
            fh = open(log_name, 'w')
            print("log_name: ", log_name)
            dirs = [d for d in os.listdir(cwd) if os.path.isdir(d)]
            print("cwd: ", cwd, "dirs: ", pp.pprint(dirs))
        for key, value in kwargs.items():
            print("%s = %s" % (key, value))
        if 'global_details' not in kwargs:
            global_details = 2
    else:
        if (len(args) == 2):
            fh = args[0]
            msg = args[1]
            #print "2 arguments found", fh, msg
            #for x in args:
            #    print "x: ", x
            log_msg = ts + " - " + msg + "\n"
            fh.write(log_msg)
            print(log_msg.rstrip())
            fh.flush()  # flush the file buffer
            os.fsync(fh) # sync the file buffer file, to make sure all the data is in teh file
        elif (len(args) == 3):
            # wlog(log_fh, dlvl, details, msg)
            # print "4 arguments found"
            fh = args[0]
            if (os.path.isfile(fh.name)):
                msg = args[2]
                dlvl = args[1]
                details = 2 # just set this to 2, just for certain messages
                if (dlvl <= details):
                    log_msg = ts + " - " + msg + "\n"
                    fh.write(log_msg)
                    print(log_msg.rstrip()) # print the log messages to the console as well
            fh.flush()
            os.fsync(fh)
        elif (len(args) == 4):
            # wlog(log_fh, dlvl, details, msg)
            # print "4 arguments found"
            fh = args[0]
            if (os.path.isfile(fh.name)):
                msg = args[-1]
                dlvl = args[1]
                details = args[2]
                if (dlvl <= details):
                    log_msg = ts + " - " + msg + "\n"
                    fh.write(log_msg)
                    print(log_msg.rstrip())
            fh.flush()
            os.fsync(fh)
        else:
            print("wrong number of arguments to logging function")
            print("args: ", args)

    return 0

def get_call_script_name():
    cwd = os.getcwd()  # get the current working directory
    frm = inspect.stack() # need to inspect hte stack to get the calling script
    #print "frm: ", pp.pprint(frm)
    root_fp = frm[1][1]  # filepath, filename, and filedirectory, so this is the root filepath
    #for f in frm:
        #print "f: ", f
    root_dir = ntpath.dirname(root_fp)
    cfg_dir = "cfg"
    script_name = ntpath.basename(root_fp) #returns the script name
    script_name = os.path.splitext(script_name)[0] # now returns the script name without the extension
    return script_name

def init_log(remove_log_fp):
    if (os.path.exists(remove_log_fp)):
        try:
            print("attempting to delete log " + remove_log_fp + "\n")
            os.remove(remove_log_fp)
        except:
            e = sys.exc_info()[0]
            print("failed to removed log file " + remove_log_fp + "\n")
            print("with error: " + str(e) + "\n")
            exit()
    else:
        print("log file : " + remove_log_fp + " does not exist")
        return