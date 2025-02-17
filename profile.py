# profile.py
# taken from https://stackoverflow.com/questions/552744/how-do-i-profile-memory-usage-in-python

import time
import os
import psutil
import inspect

import pack.inputs.control as ctrl


def elapsed_since(start):
    #return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))
    elapsed = time.time() - start
    if elapsed < 1:
        return str(round(elapsed*1000,2)) + "ms"
    if elapsed < 60:
        return str(round(elapsed, 2)) + "s"
    if elapsed < 3600:
        return str(round(elapsed/60, 2)) + "min"
    else:
        return str(round(elapsed / 3600, 2)) + "hrs"


def get_process_memory():
    process = psutil.Process(os.getpid())
    mi = process.memory_info()
    return mi.rss, mi.vms


def format_bytes(bytes):
    if abs(bytes) < 1000:
        return str(bytes)+"B"
    elif abs(bytes) < 1e6:
        return str(round(bytes/1e3,2)) + "kB"
    elif abs(bytes) < 1e9:
        return str(round(bytes / 1e6, 2)) + "MB"
    else:
        return str(round(bytes / 1e9, 2)) + "GB"


def profile(func, *args, **kwargs):

    def wrapper(*args, **kwargs):
        rss_before, vms_before = get_process_memory()
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = elapsed_since(start)
        rss_after, vms_after = get_process_memory()
        print("Profiling: {:>20}  RSS: {:>8} | VMS: {:>8} | time: {:>8}"
            .format("<" + func.__name__ + ">",
                    format_bytes(rss_after - rss_before),
                    format_bytes(vms_after - vms_before), elapsed_time) )
        with open(ctrl.memFile, 'a+') as memFile:
            memFile.write("Profiling: {:>20}  RSS: {:>8} | VMS: {:>8} | time: {:>8}".format("<" + func.__name__ + ">", format_bytes(rss_after - rss_before), format_bytes(vms_after - vms_before), elapsed_time) )
        return result

    if inspect.isfunction(func):
        return wrapper
    elif inspect.ismethod(func):
        return wrapper(*args,**kwargs)
