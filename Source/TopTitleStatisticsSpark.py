#!/usr/bin/env python
# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopTitleStatistics")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1)

def map_stage(item):
    v = int(item.strip("\n").split("\t")[1])
    return v

lines = lines.map(map_stage)
lines = lines.collect()


outputFile = open(sys.argv[2], "w")

ans1 = sum(lines) // len(lines)
ans2 = sum(lines)
ans3 = min(lines)
ans4 = max(lines)
ans5 = sum([(x-ans1)**2 for x in lines]) // len(lines)

outputFile.write('Mean\t%s\n' % ans1)
outputFile.write('Sum\t%s\n' % ans2)
outputFile.write('Min\t%s\n' % ans3)
outputFile.write('Max\t%s\n' % ans4)
outputFile.write('Var\t%s\n' % ans5)

outputFile.close()

sc.stop()

