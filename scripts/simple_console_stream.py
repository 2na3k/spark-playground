from pyspark.sql import SparkSession, DataFrame

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import (
    StructField,
    StructType,
    StringType,
    IntegerType,
    TimestampType,
)
from pyspark.sql.avro.functions import from_avro
import pyspark.sql.functions as F

import os
import json

chkp_location = str(os.getcwd()) + "/chkp_location"

schema = {
	"namespace": "example.avro",
	"type": "record",
	"name": "User",
	"fields": [
		{
			"name": "name",
			"type": "string"
		},
		{
			"name": "height",
			"type": {
				"type": "bytes",
				"logicalType": "decimal",
				"precision": 38,
				"scale": 6
			}
		}
	]
}

string_schema = json.dumps(schema)

def resolve_dependencies() -> str:
    """
    Assume that I always run from the root of the directories
    """
    deps = []
    current_directory = os.getcwd()
    print("current dir: {}".format(current_directory))
    for dirpath, dirnames, filenames in os.walk(current_directory + "/jars"):
        deps.extend(filenames)

    final_list = [current_directory + "/jars/" + jar for jar in deps]
    return ",".join(final_list)


# Kafka Consumer settings for Confluent Cloud
kafka_config = {
    "kafka.bootstrap.servers": "localhost:9094",
    "subscribe": "super-new-topic",
    "startingOffsets": "latest",  # To start from the earliest message
    "kafka.sasl.mechanism": "PLAIN",
    "failOnDataLoss": "false",
    "spark.streaming.stopGracefullyOnShutdown": True,
    # extra config: if the thing is https
    # 'kafka.security.protocol': 'SASL_SSL',
    # "kafka.ssl.endpoint.identification.algorithm" :  "https",
    # 'kafka.sasl.jaas.config': f'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="{os.getenv("KAFKA_API_KEY")}" password="{os.getenv("KAFKA_API_SECRET")}";',
}


def get_spark_session() -> SparkSession:
    deps = resolve_dependencies()
    print("dependencies str: {}".format(deps))
    spark = (
        SparkSession.builder.appName("")
        .config("spark.jars", deps)
        .config("spark.driver.extraClassPath", deps)
        # .master("spark://localhost:7077")
        .master("local[*]")
        .getOrCreate()
    )
    spark.conf.set(
        "spark.sql.streaming.stateStore.providerClass",
        "org.apache.spark.sql.execution.streaming.state.RocksDBStateStoreProvider",
    )
    spark.conf.set(
        "spark.sql.streaming.checkpointLocation", chkp_location
    )
    return spark


def load_source(spark) -> DataFrame:
    """
    Load data sink from source
    """
    return spark.readStream.format("kafka").options(**kafka_config).load()


def upsert_sink(spark, df):
    def for_each_batch_fn(df, epoch_id):
        df.show()
    (
        df
        .withColumn("avro_decoded", from_avro(F.col("value"), string_schema))
        .selectExpr("avro_decoded.*")
        .writeStream
        .format("console")
        .trigger(processingTime='5 seconds')
        .start()
        .awaitTermination()
    )


def main():
    spark = get_spark_session()
    df = load_source(spark)
    upsert_sink(spark, df)


if __name__ == "__main__":
    main()
