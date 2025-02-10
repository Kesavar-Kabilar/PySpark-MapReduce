# Spark MapReduce - Docker

## Overview 

This project explores the analysis of Wikipedia datasets, including page titles and link structures, using big data technologies. 

1. Docker containers provide a standardized development environment for consistent execution. 
2. Apache Spark, a distributed computing system, is used to implement MapReduce algorithms for efficient data processing.

## Big Data

This project tackles big data challenges by processing a substantial Wikipedia dataset, comprised of page titles and the network of links between pages.  This data is split into five distinct analytical tasks, each focusing on a different aspect:  analyzing word frequencies within titles, calculating statistics on those frequencies, identifying pages without incoming links (orphans), determining the most popular linked-to pages, and ranking pages within a user-defined "league" based on their popularity.  These exercises demonstrate how large datasets can be broken down for targeted analysis using distributed computing.

## Docker Environment

This project leverages Docker to create a consistent and reproducible development environment.  A Dockerfile is provided to build an image containing all the necessary dependencies, including Spark, Python, and other utilities.  The following Docker commands are used:

*   `docker build -t mp5 -f Dockerfile .`: This command builds the Docker image.  `-t mp5` tags the image with the name "mp5". `-f Dockerfile` specifies the Dockerfile to use for the build (in this case, named "Dockerfile").  The `.` indicates that the build context (the directory containing the Dockerfile) is the current directory.  A separate `DockerfileMac` is provided for Mac users, and the corresponding build command would be `docker build -t mp5 -f DockerfileMac .`.

*   `docker run -v <PATH_TO_LOCAL_REPO>:/MP5_SparkMapReduce_Template --name mp5-cntr -it mp5`: This command runs a Docker container based on the "mp5" image.  `-v <PATH_TO_LOCAL_REPO>:/MP5_SparkMapReduce_Template` mounts a volume, linking your local repository (replace `<PATH_TO_LOCAL_REPO>` with the actual path) to `/MP5_SparkMapReduce_Template` inside the container. This ensures that changes you make to your code locally are reflected inside the container, and vice-versa.  `--name mp5-cntr` assigns the name "mp5-cntr" to the container.  `-it` allocates a pseudo-TTY connected to stdin and keeps it open, even if not attached, and keeps STDIN open so you can interact with the container. `mp5` specifies the image to use for the container.  An additional command, `docker run -v <PATH_TO_LOCAL_REPO>:/MP5_SparkMapReduce_Template -e JAVA_TOOL_OPTIONS="-XX:UseSVE=0" --name mp5-cntr -it mp5`, is provided to address a specific issue with some systems.

The Dockerfile itself sets up the environment:

*   It starts with the `ubuntu:22.04` base image.
*   Installs essential packages like Java (OpenJDK 21), `curl`, `wget`, `git`, `zip`, `unzip`, `vim`, `expect`, and Python 3.
*   Downloads and installs Hadoop 3.3.6, setting necessary environment variables.
*   Downloads and installs Apache Spark 3.5.1, also setting required environment variables.
*   Configures `vim` with a dark background.
*   Sets the `PYSPARK_PYTHON` environment variable to use Python 3.

This Docker setup ensures that all team members use the same software versions and configurations, minimizing potential compatibility issues and simplifying the development and testing process.

## Apache Spark

Apache Spark is the core distributed computing framework used in this project. It provides the necessary tools for processing large datasets in a parallel and efficient manner.  We utilize the PySpark module, which allows us to interact with Spark using Python. Key components and methods used include:

*   **`SparkConf`:**  This class is used to configure the Spark application.  It allows setting various parameters, such as the application name and the amount of memory to allocate.  For example, you might set the app name with `SparkConf().setAppName("MySparkApp")`.

*   **`SparkContext`:**  The `SparkContext` is the entry point to Spark functionality.  It represents the connection to the Spark cluster and is used to create RDDs (Resilient Distributed Datasets), the fundamental data structure in Spark. A `SparkContext` is typically created using a `SparkConf` object.

*   **`map(function)`:** The `map` transformation applies a given function to each element of an RDD, returning a new RDD with the results. It's a one-to-one transformation.  For instance, `rdd.map(lambda x: x * 2)` would multiply each element in `rdd` by 2.

*   **`reduce(function)`:** The `reduce` action aggregates all elements of an RDD into a single value using a given commutative and associative function.  For example, `rdd.reduce(lambda x, y: x + y)` would sum all elements in `rdd`.

*   **`flatMap(function)`:** Similar to `map`, but `flatMap` applies a function that returns a list to each element of the RDD and then *flattens* the results into a single RDD.  This is useful for operations like tokenization, where you want to transform one element into multiple elements. For example, if you have an RDD of sentences, `rdd.flatMap(lambda x: x.split())` would produce an RDD of individual words.

*   **`reduceByKey(function)`:** This transformation operates on RDDs of key-value pairs. It groups the values with the same key and then applies the given function to reduce the values for each key into a single value.  For instance, if `rdd` contains pairs like `("a", 1)`, `("b", 2)`, and `("a", 3)`, then `rdd.reduceByKey(lambda x, y: x + y)` would produce `("a", 4)` and `("b", 2)`.  This is a fundamental operation in MapReduce.

These PySpark methods are used extensively in the exercises to process the Wikipedia datasets, demonstrating the core principles of distributed data processing with Spark.

## Tasks

This project is divided into five distinct tasks, each designed to exercise different aspects of Spark's MapReduce capabilities and data processing techniques.

**Task 1: Top Titles (TitleCountSpark.py)**

This task focuses on analyzing Wikipedia titles to determine the most frequent words.  It involves reading the title data, tokenizing the titles into individual words, converting words to lowercase, removing common "stop words," and then counting the occurrences of each word.  Finally, it identifies and outputs the top 10 most frequent words. This task demonstrates text processing and basic aggregation using Spark.

To run Task 1 Use Command: spark-submit TitleCountSpark.py stopwords.txt delimiters.txt dataset/titles/ partA

**Task 2: Top Title Statistics (TopTitleStatisticsSpark.py)**

Building upon the results of Task 1, this task calculates descriptive statistics for the top words. It takes the output of Task 1 (the top 10 words and their counts) as input and computes the mean, sum, minimum, maximum, and variance of the word counts. This task further explores data analysis by calculating statistical measures on aggregated data.

To run Task 2 Use Command: spark-submit TopTitleStatisticsSpark.py partA partB

**Task 3: Orphan Pages (OrphanPagesSpark.py)**

This task shifts the focus to analyzing the link structure of Wikipedia. It aims to identify "orphan pages," defined as pages that have no incoming links from other pages. The input data represents the links between pages. The task requires processing this link data to determine which pages are not referenced as targets of any links, thus identifying the orphans. This task demonstrates graph processing concepts in Spark.

To run Task 3 Use Command: spark-submit OrphanPagesSpark.py dataset/links/ partC

**Task 4: Top Popular Links (TopPopularLinksSpark.py)**

Similar to Task 3, this task works with the Wikipedia link data. However, instead of finding orphan pages, it aims to find the most popular pages, where popularity is measured by the number of incoming links.  The task processes the link data to count the number of incoming links for each page and then identifies and outputs the top 10 most popular pages. This task further explores link analysis and aggregation in Spark.

To run Task 4 Use Command: spark-submit TopPopularLinksSpark.py dataset/links/ partD

**Task 5: Popularity League (PopularityLeagueSpark.py)**

This task combines link analysis with ranking. It takes the Wikipedia link data as input, along with a separate list of page IDs called a "league." The goal is to determine the rank of each page in the league based on its popularity (number of incoming links).  The rank of a page is defined as the number of pages in the league with *lower* popularity.  This task requires calculating page popularity, filtering for the league pages, and then performing comparisons to determine the ranks. This task demonstrates more complex data manipulation and ranking operations using Spark.

To run Task 5 Use Command: spark-submit PopularityLeagueSpark.py dataset/links/ dataset/league.txt partE
