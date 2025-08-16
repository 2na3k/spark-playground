from kafka import KafkaProducer
import fastavro
from decimal import Decimal, localcontext
import schedule
import json
import time

from fastavro import schemaless_writer, parse_schema
import io

BOOTSTRAP_SERVER = "localhost:9094"
TOPIC_VALUE = "super-new-topic"
# SCHEMA_FILE = "./schema/customer.avsc"

# getcontext().prec = 6

# localcontext().prec = 38

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

data = [
   {
        "name": "Kevin",
        "height": Decimal("50.1")
   },
   {
        "name": "Dave",
        "height": Decimal("100.1")
   },
]

parsed_schema = parse_schema(schema)

def value_serializer(x: dict) -> bytes:
    return json.dumps(x).encode("utf-8")

def avro_serializer(x: dict) -> bytes:
    bytes_writer = io.BytesIO()
    fastavro.schemaless_writer(bytes_writer, schema, x)
    return bytes_writer.getvalue()

def another_avro_serializer(schema, data):
    bytes_writer = io.BytesIO()
    fastavro.schemaless_writer(bytes_writer, schema, data)
    return bytes_writer.getvalue()

producer = KafkaProducer(**{
    "bootstrap_servers": BOOTSTRAP_SERVER,
    "value_serializer": avro_serializer
})


def send_data():
    for message in data:
        print(f"sending message: {message}")
        producer.send(topic=TOPIC_VALUE, value=message)
        producer.flush()


if __name__ == "__main__":
    send_data()
    schedule.every(2).seconds.do(send_data)

    while True:
        schedule.run_pending()
        time.sleep(0.5)
    # print(f"parsed schema: {parse_schema}")