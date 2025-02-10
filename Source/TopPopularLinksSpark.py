#!/usr/bin/env python
# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopPopularLinks")
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

output = open(sys.argv[2], "w")

freq_sorted = dict(sorted(freq, key=lambda item: (-item[1], item[0])))
ret = list(freq_sorted.keys())[:10]
ret.sort()
                    
for word in ret:
    output.write(word+"\t"+str(freq_sorted[word])+'\n')

output.close()

sc.stop()

