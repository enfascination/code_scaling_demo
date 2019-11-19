"""
This script pulls from the input file the number of tweets, number of hastags, and number of tweets in English

It gives an example of a good approach to dealing with files that are too big to store frivolously on your harddrive. Its bottleneck is CPU.

Takes a bit longer than working on unzipped data, and plenty of RAM , but it worked on a 0.5 GB dataset instead of a 0.5 GB dataset!

Usage: python process_tweets3GOOD4CACHE.py data/filename.zst
"""

import sys
import io
import json
import zstandard as zstd
from pushshift_tweets import *

### set filename from command line
filename = sys.argv[-1]
print( filename )

### Counters
tw_count = 0
tag_counts = 0
en_lang = 0

### Iterate through compressed file
### from https://pypi.org/project/zstandard/
with open( filename, 'rb' ) as fh:
    dctx = zstd.ZstdDecompressor()
    stream_reader = dctx.stream_reader(fh)
    text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')
    for line in text_stream.readlines():
        line = raw_line_processing( line ) # <- data cleaning specific to pushshift
        tw = json.loads( line ) # <- the tweet 
        r = chug_tweet_stats( tw)
        tw_count += r[0]
        tag_counts += r[1]
        en_lang += r[2]

print( "OUTPUT" )
print( tw_count )
print( tag_counts )
print( en_lang )
