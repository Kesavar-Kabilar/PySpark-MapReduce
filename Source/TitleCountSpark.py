#!/usr/bin/env python

# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
'''Exectuion Command: spark-submit TitleCountSpark.py stopwords.txt delimiters.txt dataset/titles/ dataset/output'''

import sys
from pyspark import SparkConf, SparkContext

stopWordsPath = sys.argv[1]
delimitersPath = sys.argv[2]

print(sys.argv[3])

stopWordsList = []
delimiters = ""

with open(stopWordsPath) as f:
	for line in f:
		stopWordsList.append(line.strip("\n"))

with open(delimitersPath) as f:
    for line in f:
          delimiters += line.strip("\n")

conf = SparkConf().setMaster("local").setAppName("TitleCount")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[3], 1)

def map_stage(item, stopWordsList=stopWordsList, delimiters=delimiters):
    freq = {}
    word = ""
    for char in item.lower().strip():
        if char not in delimiters:
            word += char
        else:
            if word not in stopWordsList and word != "":
                freq[word] = freq.get(word.lower(), 0) + 1
            word = ""
    if word not in stopWordsList and word != "":
        freq[word] = freq.get(word.lower(), 0) + 1
    
    return [(key, value) for key, value in freq.items()]

def reduce_stage(a, b):
    return a + b

lines = lines.flatMap(map_stage)
freq = lines.reduceByKey(reduce_stage)

freq = freq.collect()

outputFile = open(sys.argv[4],"w")

freq_sorted = dict(sorted(freq, key=lambda item: (-item[1], item[0])))
ret = list(freq_sorted.keys())[:10]
ret.sort()
                    
for word in ret:
    outputFile.write(word+"\t"+str(freq_sorted[word])+'\n')

outputFile.close()

sc.stop()
