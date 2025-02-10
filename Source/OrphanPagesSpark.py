#!/usr/bin/env python
# Use LF instead of CRLF for end-of-line in files for Windows compatibility.

import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("OrphanPages")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1) 

def map_stage(item):
    lhs, rhs = item.strip("\n").split(": ")
    return set([lhs]), set(rhs.split(" "))

def reduce_stage(a, b):
    return a[0] | b[0], a[1] | b[1]

lines = lines.map(map_stage)
lhs, rhs = lines.reduce(reduce_stage)

output = open(sys.argv[2], "w")

lhs = list(lhs)
lhs.sort()

for page in lhs:
    if page not in rhs:
        output.write(page+'\n')

output.close()

sc.stop()

