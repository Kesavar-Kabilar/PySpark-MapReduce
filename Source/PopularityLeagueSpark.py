#!/usr/bin/env python
# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
#Execution Command: spark-submit PopularityLeagueSpark.py dataset/links/ dataset/league.txt
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("PopularityLeague")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1) 

def map_stage(item):
    _, rhs = item.strip("\n").split(": ")
    rhs = rhs.split(" ")
    rhs = [(word, 1) for word in rhs]
    return rhs

def reduce_stage(a, b):
    return a + b

lines = lines.flatMap(map_stage)
freq = lines.reduceByKey(reduce_stage)

freq = freq.collect()
freq = {a[0]: a[1] for a in freq}

leagueIds = sc.textFile(sys.argv[2], 1)

def map_stage_league(item, freq=freq):
    item = item.strip("\n")
    return (item, freq.get(item, -1))

leagueIds = leagueIds.map(map_stage_league)
leagueIds = leagueIds.collect()

leagueIds = sorted(list(filter(lambda a: a[1] != -1, leagueIds)), key=lambda a: a[0])

output = open(sys.argv[3], "w")

for id_1, c_1 in leagueIds:
    counter = 0
    for id_2, c_2 in leagueIds:
        if c_2 < c_1:
            counter += 1
    output.write(id_1+"\t"+str(counter)+'\n')

sc.stop()

