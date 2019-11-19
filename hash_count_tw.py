import sys
import os
import io
import re
import json
import collections

### set analysis # from command line
if len( sys.argv[-1] ) == 1:
    analysis = int(sys.argv[-1])
else: 
    analysis = 2
#print( analysis )


def tweet_count_fn(line):
    vtw = json.loads( line.strip().strip('\x00') )
    return( 1 )

def chug_tweet_basic( tw, tweet_count=None ):
    if tw:
        tweet_count += 1
    return( tweet_count )

def chug_tweet( tw, tweet_count=None , tag_counts=None, langs=None ):
    tags = re.findall( '(#\w+)', tw['full_text'])
    tweet_count += 1
    langs[ tw['lang'] ] = langs.get( tw['lang'], 0 ) + 1
    for tag in tags:
        tag_counts[tag] = tag_counts.get(tag, 0) + 1
    return( tweet_count, tag_counts, langs )

def chug_tweet2( line ):
    line =  line.strip().strip('\x00') 
    tw = json.loads( line )
    try:
        tags = re.findall( '(#\w+)', tw['full_text'])
    except:
        print( tw )
    tweet_count = 1
    lang = tw['lang']
    return( (tweet_count, len(tags), lang) )

def chug_tweet3( line ):
    line =  line.strip().strip('\x00')
    try:
        tw = json.loads( line )
    except:
        print( line )
        throw
    tags = re.findall( '(#\w+)', tw['full_text'])
    tweet_count = 1
    lang = 1 if tw['lang'] == 'en' else 0
    return( (tweet_count, len(tags), lang) )

def chug_tweet4( tw ):
    tags = re.findall( '(#\w+)', tw['full_text'])
    tweet_count = 1
    lang = 1 if tw['lang'] == 'en' else 0
    return( (tweet_count, len(tags), lang) )


if analysis == 1:
    ### takes over 4 minutes and over 50GB of RAM (on a 6.5GB dataset tht is 0.5GB compressed), and it crashes.
    ###  How is 50GB possible on a 6.5 GB dataset? 
    vtweets = json.load( open( "data/TW_verified_2019-06-02" ) )
    print( len( vtweets ) )
elif analysis == 2:
    ### takes only 1:30 minutes, and only 8MB of RAM.
    ###  How is 8MB possible on a 6.5 GB dataset? 
    tw_count = 0
    tag_counts = 0
    en_lang = 0
    with open( "data/TW_verified_2019-06-02" ) as tweets:
        for line in tweets:
            r = chug_tweet3( line)
            tw_count += r[0]
            tag_counts += r[1]
            en_lang += r[2]
    print( tw_count )
    print( tag_counts )
    print( en_lang )
elif analysis == 3:
    ### Takes a bit longer, and plenty of RAM
    ###  But it worked on a 0.5 GB dataset instead of a 0.5 GB dataset!, 
    import zstandard as zstd

    ### Counters
    tw_count = 0
    tag_counts = 0
    en_lang = 0

    ### Iterate through compressed file
    ### from https://pypi.org/project/zstandard/
    with open( "data/TW_verified_2019-06-02.zst", 'rb') as fh:
        dctx = zstd.ZstdDecompressor()
        stream_reader = dctx.stream_reader(fh)
        text_stream = io.TextIOWrapper(stream_reader, encoding='utf-8')
        for line in text_stream.readlines():
            r = chug_tweet3( line)
            tw_count += r[0]
            tag_counts += r[1]
            en_lang += r[2]
    print( tw_count )
    print( tag_counts )
    print( en_lang )
elif analysis == 4:
    ### https://medium.com/@ageitgey/quick-tip-speed-up-your-python-data-processing-scripts-with-process-pools-cf275350163a
    import concurrent.futures

    tw_count = 0
    def process_json(line, tw_count=tw_count):
        vtw = json.loads( line.strip().strip('\x00') )
        tw_count = chug_tweet_basic( vtw, tw_count )
        return( tw_count)

    with concurrent.futures.ThreadPoolExecutor(max_workers = 10) as executor:
        # Get a list of files to process
        tweets = open( "data/TW_verified_2019-06-02" )

        executor.map(process_json, tweets.readlines(), chunksize=1000)
        # Process the list of files, but split the work across the process pool to use all CPUs!
        #for tweet, thumbnail_file in zip(image_files, executor.map(process_json, image_files)):
            #print(f"A thumbnail for {image_file} was saved as {thumbnail_file}")
    print("parallel 2", tw_count )
elif analysis == 5:
    ### from https://stackoverflow.com/questions/9786102/how-do-i-parallelize-a-simple-python-loop
    from joblib import Parallel, delayed

    tw_count = 0

    def process_json(line, tw_count=tw_count):
        vtw = json.loads( line.strip().strip('\x00') )
        tw_count = chug_tweet_basic( vtw, tw_count )
        return( tw_count)

    tweets = open( "data/TW_verified_2019-06-02" )
    results = Parallel(n_jobs=10)(delayed(process_json)(i) for i in tweets.readlines())
    print(sum(results))
    print( tw_count) 
elif analysis == 6:
    print( "mp approach ")
    ### from https://stackoverflow.com/questions/6832554/multiprocessing-how-do-i-share-a-dict-among-multiple-processes
    import multiprocessing as mp

    tw_count = 0
    tag_counts = {}
    langs = {}

    def process_json(line, tw_count=tw_count, tag_counts=tag_counts, langs=langs ):
        vtw = json.loads( line.strip().strip('\x00') )
        #tw_count = chug_tweet_basic( vtw, tw_count )
        tw_count, tag_counts, langs  = chug_tweet( vtw, tw_count, tag_counts, langs )
        return( tw_count, tag_counts, langs)

    pool = mp.Pool( mp.cpu_count() )
    with open( "data/TW_verified_2019-06-02" ) as tweets:
        results = pool.map( chug_tweet3, tweets, chunksize=10000 )
    pool.close()

    #transpose results
    results = list( zip( *results ) )
    tw_count = sum(results[0])
    tag_count = sum(results[1])
    langs = collections.Counter( results[2] ) 

    print( tw_count )
    print( tag_count )
    print( langs.most_common( 10 ) )
elif analysis == 7:
    print("json lines approach")
    import jsonlines
    tw_count = 0
    tag_count = 0
    en_lang  = 0
    with jsonlines.open( "data/TW_verified_2019-06-02") as reader:
        for tweet in reader:
            r = chug_tweet4( tweet )
            tw_count += r[0]
            tag_count += r[1]
            en_lang += r[2]
    print( tw_count )
    print( tag_count )
    print( en_lang )
elif analysis == 8:
    print( "pp approach")
    import pp
    job_server = pp.Server()
    print("Starting pp with", job_server.get_ncpus(), "workers")

    tw_count = 0
    tag_counts = {}
    langs = {}
    tweets = open( "data/TW_verified_2019-06-02" )

    jobs = [(tw, job_server.submit(tweet_count_fn,(tw))) for tw in tweets.readlines()]
    twtotal = 0
    for tw, job in jobs:
        twtotal += job()
    print( twtotal )
    job_server.print_stats()
elif analysis == 9:
    ### takes 20 seconds
    ### solution from https://www.blopig.com/blog/2016/08/processing-large-files-using-python/
    ### it uses good chunking, a smart approach to per-process ffile access
    import multiprocessing as mp,os

    tw_file = "data/TW_verified_2019-06-02" 

    def process_wrapper(chunkStart, chunkSize):
        resp = []
        with open(tw_file, 'rb') as f:
            ### have to read in binary for seek to work
            f.seek(chunkStart, 0)
            lines = f.read(chunkSize).splitlines()
            for line in lines:
                line = str( line, 'utf-8' )
                result = chug_tweet3(line)
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

    #init objects
    pool = mp.Pool( mp.cpu_count())

    #create jobs
    jobs = []
    job_count = 0
    for chunkStart,chunkSize in chunkify(tw_file):
        jobs.append( pool.apply_async(process_wrapper,(chunkStart,chunkSize)) )
        job_count += 1

    print( "jobs:", job_count)
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

    print( tw_count )
    print( tag_count )
    print( en_lang )
elif analysis == 0:
    import multiprocessing as mp

    tw_file = "data/TW_verified_2019-06-02" 

    def process_wrapper(lineByte):
        with open( tw_file ) as f:
            f.seek(lineByte)
            line = f.readline()
            result = chug_tweet3(line)
        return( result )

    #init objects
    pool = mp.Pool( mp.cpu_count() )
    jobs = []

    #create jobs
    with open( tw_file) as f:
        nextLineByte = f.tell()
        line = f.readline()
        while line:
            jobs.append( pool.apply_async(process_wrapper,(nextLineByte, )) )
            nextLineByte = f.tell()
            line = f.readline()

    #wait for all jobs to finish
    tw_count = 0
    tag_count = 0
    en_lang  = 0

    for job in jobs:
        r = job.get()
        tw_count += r[0]
        tag_count += r[1]
        en_lang += r[2]


    #clean up
    pool.close()

    print( tw_count )
    print( tag_count )
    print( en_lang )

