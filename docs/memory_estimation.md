# Memory optimization

## Memory model:
- [Overall memory model](https://luminousmen.com/post/dive-into-spark-memory)
- [On-heap memory model](https://stackoverflow.com/questions/63565290/spark-memory-fraction-vs-young-generation-old-generation-java-heap-split)
- [Random docs](https://community.cloudera.com/t5/Community-Articles/Spark-Memory-Management/ta-p/317794)

### Memory estimation
Glue spec (since I can't touch the executor config in Glue):

| Worker type | Spec |
| --- | --- |
| G. 1x | `spark.executor.memory = 10gb`, `spark.driver.memory = 10gb`, `spark.executor.core = 4`|
| G. 2x | `spark.executor.memory = 20gb`, `spark.driver.memory = 20gb`, `spark.executor.core = 8`|

Quick math, assuming that the `spark.executor.memory = 20gb`:
- Reserved memory = 300mb > sum of the Spark Memory + User memory = 19.7gb
- Spark united memory:
  - Can setup the `spark.memory.fraction`, default by 0.6 to split between the user memory and Spark memory
  - User memory (default = 40% of the sum) = 19.7 * 40% = 7.88gb
  - Spark memory (default = 60% of the sum) = 19.7 * 60% = 11.82gb
    - To fix the ratio, tune the `spark.memory.storageFraction`, default by 0.5 
    - Storage memory pool = 11.82 / 2 = 5.91gb
    - Also the executor memory pool = 5.91gb
    - Both storage memory and executor memory are dynamically allocated by Spark
- Memory overhead: at least 10% of executor memory, minimum by 384mb (in this case: 2gb)