"""
This script pulls from the input file the number of tweets, number of hastags, and number of tweets in English

It gives an example of a standard approach to dealing with files that scales fairly well in RAM for low complexity. Its bottleneck is CPU

Usage: python process_tweets2GOOD.py data/filename
"""

import sys
import json
from pushshift_tweets import *

### set filename from command line
filename = sys.argv[-1]

### takes only 1:30 minutes, and only 8MB of RAM.
###  How is 8MB possible on a 6.5 GB dataset? 
tw_count = 0
tag_counts = 0
en_lang = 0

with open( filename ) as tweets:
    for line in tweets:
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
