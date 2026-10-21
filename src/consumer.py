"""Consume stock ticks from Kafka and land them in S3.

Each message is written as its own JSON object so that an AWS Glue crawler can
infer the schema and Amazon Athena can query the data in place.
"""

import json
import os

from kafka import KafkaConsumer
from s3fs import S3FileSystem

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "demo_test")
S3_BUCKET = os.environ["S3_BUCKET"]
S3_PREFIX = os.getenv("S3_PREFIX", "stock_ticks")


def main() -> None:
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS.split(","),
        value_deserializer=lambda raw: json.loads(raw.decode("utf-8")),
    )
    s3 = S3FileSystem()
    print(f"Writing messages from '{TOPIC}' to s3://{S3_BUCKET}/{S3_PREFIX}/")

    for count, message in enumerate(consumer):
        with s3.open(f"s3://{S3_BUCKET}/{S3_PREFIX}/stock_{count}.json", "w") as file:
            json.dump(message.value, file)


if __name__ == "__main__":
    main()
