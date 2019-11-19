import re

def raw_line_processing( line ):
    line =  line.strip().strip('\x00')
    return(line ) 

def chug_tweet_stats( tw ):
    """
    Takes a tweet object and returns the number of tweets it is (1), the number of hashtags it has, and 1/0 for whether it is in english
    """
    ### get stats:
    tweet_count = 1
    tags = re.findall( '(#\w+)', tw['full_text'])
    lang = 1 if tw['lang'] == 'en' else 0
    return( (tweet_count, len(tags), lang) )
