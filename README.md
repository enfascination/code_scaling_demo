# Writing code that scales

This is a demo for walking you through the kinds of things that go wrong when you are analyzing big datasets, and what you can do about them. We pull down a large dataset of tweets and calculate some simple descriptives over them.  We do this several times in several ways, demonstrate the naive approach, the standard approach, the disk-space friendly approach, and the fully parallelized approach in turn.

## Presentation
In addition to being a code demo, their is also a lecture on high-level strategies for scaling your data science code.  You'll find it in 
`presentations/Code_scaling_strategies.pdf`.

# Getting started
If you can, get as far as **Peek at the data** on your own.  Otherwise, show up early for setup help.

## Prereqs
*  You have to know how to open and type things into your shell/terminal/Terminal.app/PowerShell/bash/command line
*  You have to know how to clone a repo and navigate to it in shell
*  You have to be able to install command line software, namely `zstandard`/`zstd`
*  You need Python and its ecosystem
   *  You need `pip`. Type it in shell and see what happens)
*  You probably need a *package manager*: apt, conda, homebrew, ports, or something for windows.
   *  Probably go with `anaconda` if on mac or windows

## Installations
zstandard is a fancy zip that pushshift uses to compress its tweets.  You need both the commmand line tool and python library to work with that data in this demo..
  *  Using package manager, install command line tool [zstd](https://www.google.com/search?q=install+zstd)
  *  And for within-Python access to zstd, in your terminal type
```shell
pip install zstandard
```

## Explore the potential data
Go to https://files.pushshift.io

## Pull this repo
```
git clone https://github.com/enfascination/code_scaling_demo.git
cd code_scaling_demo
```

## Download and prep the data
The code below assumes file dated `2019-10-20`, but you can use any date from those listed on pushshift's [daily listing of tweets by verfiied users](https://files.pushshift.io/twitter/verified_feed).

In your terminal, run the following commands one at a time
```shell
mkdir data
cd data
curl -O http://files.pushshift.io/twitter/verified_feed/TW_verified_2019-10-20.zst
zstd -dvf TW_verified_2019-10-20.zst
cd ..
```

## Peek at the data
Check out the files sizes of these giant files, the first part of the first line, and the total number of lines (tweets): 
```shell
ls -lah data/                             # <- how big are the zipped and unzipped files?
head -c 1000 data/TW_verified_2019-10-20  # <- what's in the file?
wc -l data/TW_verified_2019-10-20         # <- how many tweets are in the file?
```
The format of this data is the JSON Lines format, one json object per line (each a tweet)

# Running the analysis, several ways
## Read the data the wrong way
**WARNING** This could crash your machine, and will definitely slow it down.  Be prepared to shut it down when you start it.
```shell
python process_tweets1BAD.py data/TW_verified_2019-10-20
```

## Read the data a decent way
```shell
time python process_tweets2GOOD.py data/TW_verified_2019-10-20
# ^ preceding a line with time makes it print out how long a command took to run.  You want to watch the last number, the wall clock time. 
```
_Questions to ask yourself_:
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
```shell
time python process_tweets3GOOD4CACHE.py data/TW_verified_2019-10-20.zst
                                                                    # ^ don't forget this suffix
```
_Questions to ask yourself_:
  *  Q: How long did it take to run? 
  *  Q: How much RAM did it demand of your machine?
  *  Q: How much smaller was the input file this time?
  *  Q: What if even the zipped file is too big?
     *  A: Could have streamed straight from pushshift.
        *  This is kind of rude if you don't own the other machine
        *  And it makes network bandwidth a bottleneck

## The fastest type of way to read data: parallelized
```shell
time python process_tweets4GREAT.py data/TW_verified_2019-10-20
```
_Questions to ask yourself_:
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

----------
# TODO

 *  Improve instructions for vanilla setup
   *  either assume conda or provide a cross platform gui installation of zstandard
   *  windows instructions (powershell, that free ubuntu VM?)
