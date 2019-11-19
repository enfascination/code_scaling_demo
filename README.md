# Writing code that scales

This is a demo for walking you through the kinds of things that go wrong when you are analyzing big datasets, and what you can do about them. We pull down a large dataset of tweets and calculate some simple descriptives over them.  We do this several times in several ways, demonstrate the naive approach, the standard approach, the disk-space friendly approach, and the fully parallelized approach in turn.


# Getting started
## Prepare your environment with the right packages
  *  Using apt, conda, homebrew, ports, whatever, install command line tool [zstd](https://www.google.com/search?q=install+zstd)
  *  In your terminal
```shell
pip install zstandard
```

## Explore the potential data
Go to https://files.pushshift.io

## Download and prep the data
The code below assumes file dated `2019-10-20`, but you can use any date from those listed on pushshift's [daily listing of tweets by verfiied users](https://files.pushshift.io/twitter/verified_feed).

In your terminal
```shell
mkdir data
cd data
wget https://files.pushshift.io/twitter/verified_feed/TW_verified_2019-10-20.zst data/
zstd -dvf TW_verified_2019-10-20.zst
cd ..
```

## Peek at the data
Check out the first part of the first line of this giant file by typing
```shell
ls -lah data/
head -c 1000 data/TW_verified_2019-10-20
wc -l data/TW_verified_2019-10-20
```
The format of this data is the JSON Lines format, one json object per line (each a tweet)

# Running the analysis, several ways
## Read the data the wrong way
***WARNING*** This could crash your machine, and will definitely slow it down.  Be prepared to shut it down when you start it.
```python
python process_tweets1BAD.py data/TW_verified_2019-10-20
```

## Read the data a decent way
```python
time python process_tweets2GOOD.py data/TW_verified_2019-10-20
```
Questions to ask yourself:
  *  Q: How long did it take to run? 
  *  Q: How much RAM did it demand of your machine?
  *  Q: What are the upsides of this approach?
     *  A: Standard
     *  A: Straightforward
     *  A: Scales pretty well
  *  Q: What are the downsides of this approach?
     *  A: Just uses one core; could be faster
     *  A: Have to store the whole uncompressed dataset

## Read the data a good way for storage constraints
```python
time python process_tweets3GOOD4CACHE.py data/TW_verified_2019-10-20.zst
                                                                    # ^ don't forget this suffix
```
Questions to ask yourself:
  *  Q: How long did it take to run? 
  *  Q: How much RAM did it demand of your machine?
  *  Q: How much smaller was the input file this time?
  *  Q: What if even the zipped file is too big?
     *  A: Could have streamed straight from pushshift.
        *  This is kind of rude if you don't own the other machine
        *  And it makes network bandwidth a bottleneck

## The fastest type of way to read data: parallelized
```python
time python process_tweets4GREAT.py data/TW_verified_2019-10-20
```
Questions to ask yourself:
  *  Q: How long did it take to run? 
  *  Q: How much RAM did it demand of your machine?
  *  Q: What was your CPU utilization (How many and how much CPU was used)?
  *  Q: What are the upsides of this approach?
     *  A: Really scales well.
  *  Q: What are the downsides of this approach?
     *  A: More complicated (Certainly took me a while to figure out)
        *  Especially for this use case: reading a large file
        *  (There are better uses for parellelism than reading files)
     *  A: The bottleneck becomes file IO: the low-level fact that we have to read data in from a file

