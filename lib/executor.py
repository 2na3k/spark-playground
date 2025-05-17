from abc import ABC, abstractmethod
from pyspark.sql import SparkSession, DataFrame
from lib.schema import ExecutorConfig


class Executor(ABC):
    def __init__(self, spark: SparkSession, config: ExecutorConfig = None):
        self.spark = spark
        self.config = config

    @abstractmethod
    def read():
        raise NotImplementedError

    @abstractmethod
    def write():
        raise NotImplementedError
