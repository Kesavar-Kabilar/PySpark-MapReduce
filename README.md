# Spark MapReduce - Docker

## Overview 

This project analyzes Wikipedia datasets, including page titles and link structures, using big data technologies.

*   **Big Data:** This assignment utilizes a substantial Wikipedia dataset, including page titles and link structures, representing a typical big data challenge.  Distributed processing techniques, like those provided by Spark, are essential for efficiently analyzing this volume of information.

*   **Docker:** Docker containers provide a consistent and reproducible environment for both development and grading, crucial because the autograder runs offline.  All dependencies are pre-packaged within the Docker image, eliminating compatibility issues and ensuring consistent execution.

*   **Apache Spark:** Apache Spark is the core distributed computing framework, enabling efficient data processing through MapReduce algorithms.  Spark's distributed computing capabilities, along with transformations like map, flatMap, and reduceByKey, are used to perform various data analysis tasks on the Wikipedia data.

## Big Data

This project tackles big data challenges by processing a substantial Wikipedia dataset, comprised of page titles and the network of links between pages.  This data is split into five distinct analytical tasks, each focusing on a different aspect:  analyzing word frequencies within titles, calculating statistics on those frequencies, identifying pages without incoming links (orphans), determining the most popular linked-to pages, and ranking pages within a user-defined "league" based on their popularity.  These exercises demonstrate how large datasets can be broken down for targeted analysis using distributed computing.

## Docker Environment

This project utilizes Docker to ensure a consistent and reproducible development and grading environment.  Because the autograder runs within a Docker container *without internet access*, all dependencies and the execution environment must be self-contained.  Docker addresses this by packaging all required software, including Java, Hadoop, Spark, Python, and necessary utilities, into a single image.  This eliminates potential issues arising from differing system configurations or missing dependencies on individual developer machines or the grading server.  Furthermore, the Docker setup restricts file system access to the project directory, mirroring the autograder's constraints and encouraging code that adheres to the assignment's limitations.

The following Docker commands are used to build and run the container:

Windows: 

```bash
docker build -t mp5 -f Dockerfile .
```

Mac: 

```bash
docker build -t mp5 -f DockerfileMac . 
``` 

This command builds the Docker image. -t mp5 tags the image with the name "mp5". -f Dockerfile specifies the Dockerfile to use for the build.

```bash
docker run -v <PATH_TO_LOCAL_REPO>:/MP5_SparkMapReduce_Template --name mp5-cntr -it mp5
```

This command runs a Docker container based on the "mp5" image. -v <PATH_TO_LOCAL_REPO>:/MP5_SparkMapReduce_Template mounts a volume, linking your local repository to /MP5_SparkMapReduce_Template inside the container. This allows you to edit your code locally and have the changes immediately reflected within the container. --name mp5-cntr assigns the name "mp5-cntr" to the container. -it provides interactive access to the container. mp5 specifies the image to use.  The command docker run -v <PATH_TO_LOCAL_REPO>:/MP5_SparkMapReduce_Template -e JAVA_TOOL_OPTIONS="-XX:UseSVE=0" --name mp5-cntr -it mp5 is also provided as a possible solution to a specific error.

## Apache Spark

Apache Spark is the core distributed computing framework used in this project, providing the tools necessary for parallel and efficient processing of the large Wikipedia datasets.  The PySpark module facilitates interaction with Spark using Python.  Several key components and methods were crucial for completing the assignment:

*   **`SparkConf`:**  This class was used to configure each Spark application, allowing us to set the application name (e.g., `SparkConf().setAppName("TitleCount")`) which is helpful for monitoring and debugging during development and within the Docker environment.  While memory allocation wasn't explicitly configured in the provided examples, `SparkConf` would be essential for optimizing performance with larger datasets.

*   **`SparkContext`:** The `SparkContext` served as the entry point to all Spark functionality.  It established the connection to the Spark cluster (even within the single-node Docker setup) and was used to create the initial RDDs from the input data files (Wikipedia titles or links).  For example, `sc = SparkContext(conf=SparkConf())` would initialize the context.

*   **`map(function)`:**  `map` transformations were used for various data preparation steps. For instance, in the "Top Titles" task, `map` was likely used to convert each Wikipedia title into a list of words or to lowercase each word. It's a fundamental operation for transforming individual elements of the datasets.

*   **`reduce(function)`:** While `reduce` itself might not be directly used in the final solutions due to the need for key-based aggregation, the *concept* of reduction is inherent in tasks like calculating statistics (mean, sum, etc.) in "Top Title Statistics."  `reduceByKey`, however, is a very important part of the MapReduce paradigm, and is covered below.

*   **`flatMap(function)`:**  `flatMap` was essential for tasks involving tokenization.  In "Top Titles," it was likely used to split each title string into individual words, creating a flattened RDD of all words across all titles.  This transformation is crucial for turning the raw title data into a format suitable for counting word frequencies.

*   **`reduceByKey(function)`:** `reduceByKey` played a central role in aggregating counts for words or incoming links.  In "Top Titles," it would be used to count the occurrences of each word after the `flatMap` operation. Similarly, in "Top Popular Links" and "Popularity League," it would be used to count the number of incoming links for each page ID.  This method is at the heart of the MapReduce paradigm, enabling efficient aggregation of data based on keys.

These PySpark methods were instrumental in processing the Wikipedia datasets within the Docker container, enabling the implementation of the MapReduce logic for each of the five tasks.  They allowed for efficient distributed processing of the data, even within the constraints of the assignment's environment.

## Tasks

This project is divided into five distinct tasks, each designed to exercise different aspects of Spark's MapReduce capabilities and data processing techniques.

**Task 1: Top Titles (TitleCountSpark.py)**

This task focuses on analyzing Wikipedia titles to determine the most frequent words.  It involves reading the title data, tokenizing the titles into individual words, converting words to lowercase, removing common "stop words," and then counting the occurrences of each word.  Finally, it identifies and outputs the top 10 most frequent words. This task demonstrates text processing and basic aggregation using Spark.

To run Task 1 Use Command: 

```bash
spark-submit TitleCountSpark.py stopwords.txt delimiters.txt dataset/titles/ partA
```

**Task 2: Top Title Statistics (TopTitleStatisticsSpark.py)**

Building upon the results of Task 1, this task calculates descriptive statistics for the top words. It takes the output of Task 1 (the top 10 words and their counts) as input and computes the mean, sum, minimum, maximum, and variance of the word counts. This task further explores data analysis by calculating statistical measures on aggregated data.

To run Task 2 Use Command: 

```bash
spark-submit TopTitleStatisticsSpark.py partA partB
```

**Task 3: Orphan Pages (OrphanPagesSpark.py)**

This task shifts the focus to analyzing the link structure of Wikipedia. It aims to identify "orphan pages," defined as pages that have no incoming links from other pages. The input data represents the links between pages. The task requires processing this link data to determine which pages are not referenced as targets of any links, thus identifying the orphans. This task demonstrates graph processing concepts in Spark.

To run Task 3 Use Command: 

```bash
spark-submit OrphanPagesSpark.py dataset/links/ partC
```

**Task 4: Top Popular Links (TopPopularLinksSpark.py)**

Similar to Task 3, this task works with the Wikipedia link data. However, instead of finding orphan pages, it aims to find the most popular pages, where popularity is measured by the number of incoming links.  The task processes the link data to count the number of incoming links for each page and then identifies and outputs the top 10 most popular pages. This task further explores link analysis and aggregation in Spark.

To run Task 4 Use Command: 

```bash
spark-submit TopPopularLinksSpark.py dataset/links/ partD
```

**Task 5: Popularity League (PopularityLeagueSpark.py)**

This task combines link analysis with ranking. It takes the Wikipedia link data as input, along with a separate list of page IDs called a "league." The goal is to determine the rank of each page in the league based on its popularity (number of incoming links).  The rank of a page is defined as the number of pages in the league with *lower* popularity.  This task requires calculating page popularity, filtering for the league pages, and then performing comparisons to determine the ranks. This task demonstrates more complex data manipulation and ranking operations using Spark.

To run Task 5 Use Command: 

```bash
spark-submit PopularityLeagueSpark.py dataset/links/ dataset/league.txt partE
```
