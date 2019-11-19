"""
This script is supposed to from the input file the number of tweets.

But your computer will probably not be able to report that number.  This script gives an example of a standard approach for small files that does not scale to large files.  The bottleneck of this code is RAM. Pay attention to your computer's RAM usage while this runs.  If you run this, be prepared to shut it down prematurely.

Usage: python process_tweets1BAD.py data/filename

"""

import sys
import json

### set filename from command line
filename = sys.argv[-1]

### takes over 4 minutes and over 50GB of RAM (on a 6.5GB dataset tht is 0.5GB compressed), and it crashes.
###  How is 50GB possible on a 6.5 GB dataset? 
vtweets = json.load( open( filename ) )
print( len( vtweets ) )
