# Quicknote
Fine-tuning Spark in panic

## Notes
(All the thanks to Rock the JVM with [this](https://www.youtube.com/watch?v=LoFN_Q224fQ) and [this](https://www.youtube.com/watch?v=UZt_tqx4sII))


Read the query plan: https://www.youtube.com/watch?v=KnUXztKueMU

DAG concept:
- `WholeStageCodegen`: Computation within a dataframe
- `mapPartitionInternal`: forEach RDD partition
- `Exchange`: Shuffle -> If this happens, that's the bottleneck.

Random fact:
- Disk spill can be managed by setting the memory overhead ([source](https://www.clairvoyant.ai/blog/apache-spark-out-of-memory-issue))
- Can't directly set the `spark.executor.memory` in Glue directlly, must goes through the YARN by `spark.yarn.executor.memory=8gb`
- If we read CSV files, it gonna goees to the user memory ([fact](https://stackoverflow.com/questions/74586108/what-is-user-memory-in-spark)), maybe the same with write operation to serde that.
- Off-heap memory in JVM is not bounded by GC, GC only apply with on-heap




### Parallelism in Spark
- Read: 
  - [Calculate the number of parallel tasks taht can be executed](https://medium.com/@rganesh0203/calculate-the-number-of-parallel-tasks-that-can-be-executed-in-a-databricks-pyspark-cluster-a3ad5f864955#:~:text=In%20a%20Spark%20cluster%2C%20each,total%20number%20of%20CPU%20cores.).
  - [Random blog](https://www.guptaakashdeep.com/enhancing-spark-job-performance-multithreading/)
- If we setup `spark.default.parallelism`, we might change the number of tasks that can run in parallel.
- Each task is generally assigned to a single CPU core. Therefore, the number of parallel tasks is equivalent to the total number of CPU cores.


### Bucketing
- Is the method
- Is not supported by Delta Lake (what)
  - Legit reason from DBX: Have clustering, and z-ordering clustering
  
### Salting
- Is a method that can be used when the hash-key is not evenlly distributed.