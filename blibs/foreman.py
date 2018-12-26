
import os
import inspect
import subprocess
import ntpath
import sys
import re
import pprint
import shutil
import string

def search_dir(regx, fp): # this will take the first match that it finds and returns the filepath
    print("preparing to search for ", regx, " in ", fp)
    any_match = False
    all_fps = get_list_dir(fp, 3)
    # print "all_fps: ", all_fps
    pp.pprint(all_fps)
    a = re.compile(regx)
    for fp in all_fps:
        matcher = a.search(fp)  #search finds the regx anywhere in the line
        if matcher:
            any_match = True # any match was found
            print("regular expression found")
            yield fp
    if any_match == False:  # if any match was not found return None
        print("regx ", regx, " not found in fp ", fp)
        yield None

def search_dir_depth(regx, fp, search_depth): # this will take the first match that it finds and returns the filepath
    print("preparing to search for ", regx, " in ", fp)
    any_match = False
    if search_depth is None:
        all_fps = get_list_dir(fp, 3)
    else:
        all_fps = get_list_dir(fp, 3, search_depth)
    # print "all_fps: ", all_fps
    pp.pprint(all_fps)
    a = re.compile(regx)
    for fp in all_fps:
        matcher = a.search(fp)  #search finds the regx anywhere in the line
        if matcher:
            any_match = True # any match was found
            print("regular expression found")
            yield fp
    if any_match == False:  # if any match was not found return None
        print("regx ", regx, " not found in fp ", fp)
        yield None

def search_for_filename(fn, dirp, depth = -1, debug = 0):
    ret_val = []
    all_fps = get_list_dir(dirp, 3)
    for fp in all_fps:
        check_fn = os.path.basename(fp)
        if (check_fn == fn):
            ret_val.append(fp)
    return ret_val

def get_list_dir(fp, mode, depth = -1, debug = 0):  #takes a file path, a mode for what to return, and a depth for returning a list of filepaths, filenames, directory paths, or directories
    # filenames, dir names, file paths, dir paths, all paths, all names, ?structure
    ret_val = []
    loc_depth = 0
    if (debug == 1):
        print("get_list_dir fp: ", fp)
    for (dirpath, dirnames, filenames) in os.walk(fp, topdown=True):
        if (debug == 1):
            print("dirpath: ", dirpath, "dirnames: ", dirnames, "filenames: ", filenames)
        if (mode == 1):
            ret_val.extend(filenames)
        if (mode == 2):
            ret_val.extend(dirnames)
        if (mode == 3):
            for fn in filenames:
                if (debug == 1):
                    print("fn: ", fn)
                    print("fp: ", fp)
                fp = dirpath + os.sep + fn
                ret_val.append(fp)
        if (mode == 4):
            for dir in dirnames:
                dirp = dirpath + os.sep + dir
                ret_val.append(dirp)
        loc_depth += 1  #i'm not sure this works quite the way I think it does, but it's fine for depth 1, this will iterate over several folders if there are more folders there
        if (debug == 1):
            print("loc_depth: ", loc_depth)  # need to fix the depth argument
        if (loc_depth >= depth) & (depth != -1):
            break
    return ret_val

def is_file(fp, details=50):
    if (os.path.isfile(fp)):
        if (details > 10):
            print("file is file and exists: ", fp)
        return 1
    else:
        if (details > 10):
            print("filepath is not file:", fp)
        return 0

def is_dir(dirp, details=50):
    if os.path.exists(dirp):
        if (details > 10 ):
            print("dirp exists: ", dirp)
        return 1
    else:
        if (details > 10):
            print("dirp not exist: ", dirp)
        return 0

def check_create_dir(dirp, details = 50):
    if (details > 5):
        print("preparing to check create dirp: ", dirp)
    if os.path.exists(dirp) & os.path.isdir(dirp):
        return
    else:
        os.mkdir(dirp)
        return

def remove_whitespace(string, mode=0):
    # all, trailing, leading modes

    if re.match(r'^\s*$', string):
        return ""
    if (mode == 0):  # leading trailing
        print("mode 0 for remove the white space")
        new_string = string.strip()  #should remove leading and trailing whitespace
    elif (mode == 1):  # remove all whitespace from a line \s \t \n
        new_string = "".join(string.split())
        #print "new_string: ", new_string
    return new_string

class csv_file_info():
    def __init__(self, fh):
        self.fn = fh.name

def file_line_count(fp):  #convenience for getting the total number of file lines
    i = 0
    if (is_file(fp, 0) == 0):
        print("Error with object sent to file_line_count: ", sys.exc_info()[0])
        return

    else:
        with open(fp) as f:
            for i, l in enumerate(f):
                pass
    return i + 1

def try_open(fp, mode):
    try:
        fh = open(fp, mode)
        return (fh, 1)
    except:
        e = sys.exc_info()[0]
        return (e, 0)

def copy_file_list(all_fps, out_dirp):
    for fp in all_fps:
        fn = os.path.basename(fp)
        new_fp = out_dirp + os.sep + fn
        fp = re.sub(r'\\', r'/', fp)
        out_dirp = re.sub(r'\\', r'/', out_dirp)
        new_fp = re.sub(r'\\', r'/', new_fp)
        is_file(fp)
        is_dir(out_dirp)
        logger.wlog(for_log_fh, "attempting to copy: " + fp + " to \n " + new_fp)
        try:
            shutil.copyfile(fp, new_fp)
        except:
            e = sys.exc_info()
            logger.wlog(for_log_fh, "Error attempting to copy file")
            logger.wlog(for_log_fh, "Error: " + str(e))
            logger.wlog(for_log_fh, "source file: " + fp)
            logger.wlog(for_log_fh, "sink dirp: " + out_dirp)

def binary_search_recursive(li, left, right, key):
    while True:
        if left > right:
          return -1
        mid = (left + right) / 2
        if li[mid] == key:
          return mid
        if li[mid] > key:
            right = mid - 1
        else:
            left = mid + 1
        return binary_search_recursive(li, left, right, key)

def remove_list_dups_keep_order(incomingList):
    seen = set()
    seen_add = seen.add
    return [x for x in incomingList if not (x in seen or seen_add(x))]

def list_check(inString, checkList):  # ignores white space and case to check for a string, return index or -1
    index = 0
    for item in checkList:
       # strippedItem = "".join(item.split())
       # stripptedString = "".join(inString.split())
        strippedItem = ''.join(eachChar.lower() for eachChar in item if not eachChar.isspace())
        strippedString = ''.join(eachChar.lower() for eachChar in inString if not eachChar.isspace())
        if (strippedItem == strippedString):
            return index
            break
        index += 1
    return -1

def kwargs_check_assign(kwargs, key, def_value):
    if key in kwargs:
        return kwargs[key]
    else:
        return def_value

def check_assign(obj, key, default):
    if key in obj:
        return obj[key]
    else:
        return default

def get_sub_folder(fp):
    return os.path.dirname(fp)

def get_path_items(path):
    folders = []
    while 1:
        path, folder = os.path.split(path)
        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)
            break
    return folders

def remove_all_in_path(path):
    all_in_path = os.listdir(path)
    if len(all_in_path) == 0:
        print("Nothing in path to delete")
        return
    for each in all_in_path:
        try:
            print(("Trying to remove: ",each))
            shutil.rmtree(os.path.join(path,each))
        except Exception as e:
            print(("Unable to remove ",each,e))

def gen_column_letters():
    alphabet = list(string.ascii_lowercase)
    for item in alphabet:
        yield item

pp = pprint.PrettyPrinter(indent=4)
if (is_dir('./lib/')):
    for_log_fh = open('./lib/foreman.log', 'w')
else:
    for_log_fh = open('foreman.log', 'w')
