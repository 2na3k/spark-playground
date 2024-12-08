# Join optimization

What to read:
- Join strategies overview: [Join](https://plainenglish.io/blog/a-deep-dive-into-the-inner-workings-of-apache-spark-join-strategies)
- Bucketing: [The internal of SparkSQL](https://books.japila.pl/spark-sql-internals/bucketing/)

Boardcast hash join
- Broadcast the smaller dataset (often smaller than the `spark.sql.autoBroadcastJoinThreshold`) and literally do the hash join in each worker when all the key is hashed in the same partition.
  
Shuffle hash join: 
- Default join strategies
- How: First partitioned the data from join tables based on the join key, distributed the partition throughout the workers with the same join keys assigned to specific partitions, and do the single node hash join.
- Join key is skew -> going to be sort merge join

Sort merge join
- Often occurs when 
  - the distribution between the join key/partition is skew -> hash table is not reliable -> have to sort; or already sorted by the join key so the cost of sorting data is lower than the cost of shuffling data.
  - Required full outer join/left outer join -> can't perform on broadcast join
- Partitioned by the join key, distribbuted to the same partition, then sort it -> merge across partition to perform join operation
  
Broadcast nested loop join

Cartesian: 
- Loop through all of the combination of join between 2 datasets -> No