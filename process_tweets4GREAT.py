"""
This script pulls from the input file the number of tweets, number of hastags, and number of tweets in English

It gives an example of an optimized approach to dealing with files that scales fine in RAM and takes full advantage of potential CPU.  The cost is code complexity: this code is hard to understand.  That said, you don't have to understand it all: you just have to be able to spot the part that you can change.

Usage: python process_tweets4GREAT.py data/filename
"""

import os
import sys
import json
import multiprocessing as mp
from pushshift_tweets import *

### set filename from command line
filename = sys.argv[-1]

### takes 20 seconds
### it uses good chunking, a smart approach to per-process ffile access

### EDIT THIS AND ADD CODE YOU WANT PARALLELIZED
# job function
def your_fn(line):
    line = raw_line_processing( line ) # <- data cleaning specific to pushshift
    tw = json.loads( line ) # <- the tweet 
    r = chug_tweet_stats( tw)
    return( r )

# HELPER FUNCTIONS
### from https://www.blopig.com/blog/2016/08/processing-large-files-using-python/
def process_wrapper(your_fn, chunkStart, chunkSize):
    resp = []
    with open(filename, 'rb') as f:
        ### have to read in binary for seek to work
        f.seek(chunkStart, 0)
        lines = f.read(chunkSize).splitlines()
        for line in lines:
            line = str( line, 'utf-8' )
            result = your_fn(line)
            resp.append( result )
    return( resp )

def chunkify(fname,size=1024*1024):
    fileEnd = os.path.getsize(fname)
    with open(fname, 'rb') as f: ### forced to read in binary
        chunkEnd = f.tell()
        while True:
            chunkStart = chunkEnd
            f.seek(size, 1)
            f.readline()
            chunkEnd = f.tell()
            yield chunkStart, chunkEnd - chunkStart
            if chunkEnd > fileEnd:
                break

### START CODE
#init objects
pool = mp.Pool( mp.cpu_count())

#create jobs
jobs = []
job_count = 0
# Send to machine
for chunkStart,chunkSize in chunkify(filename): 
    jobs.append( pool.apply_async(process_wrapper,(your_fn, chunkStart,chunkSize)) )
    job_count += 1

### process outputs
#wait for all jobs to finish
tw_count = 0
tag_count = 0
en_lang  = 0
for job in jobs:
    job.get()
    rs = job.get()
    for r in rs:
        tw_count += r[0]
        tag_count += r[1]
        en_lang += r[2]
#clean up
pool.close()

print( "OUTPUT" )
print( tw_count )
print( tag_count )
print( en_lang )
