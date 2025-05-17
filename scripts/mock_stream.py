import datetime
import time
import random
import schedule
from json import dumps
from faker import Faker
from kafka import KafkaProducer


kafka_nodes = "localhost:9094"
myTopic = "source-wordcount"


def gen_data():
    faker = Faker()

    prod = KafkaProducer(
        bootstrap_servers=kafka_nodes,
        value_serializer=lambda x: dumps(x).encode("utf-8"),
    )
    my_data = {
        "word": faker.word(), 
        "counter": random.uniform(1, 10),
        "data_ts": str(datetime.datetime.now())
    }
    print(f"Send data: {my_data}")
    prod.send(topic=myTopic, value=my_data)

    prod.flush()


if __name__ == "__main__":
    gen_data()
    schedule.every(2).seconds.do(gen_data)

    while True:
        schedule.run_pending()
        time.sleep(0.5)
