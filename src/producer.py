"""Stream stock market ticks into Kafka.

Samples one row at a time from the historical index dataset and publishes it
as JSON to a Kafka topic, simulating a live market feed.
"""

import json
import os
from time import sleep

import pandas as pd
from kafka import KafkaProducer

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "demo_test")
DATA_PATH = os.getenv("DATA_PATH", "data/indexProcessed.csv")
INTERVAL_SECONDS = float(os.getenv("INTERVAL_SECONDS", "1"))


def main() -> None:
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS.split(","),
        value_serializer=lambda record: json.dumps(record).encode("utf-8"),
    )
    df = pd.read_csv(DATA_PATH)
    print(f"Streaming {len(df):,} rows to topic '{TOPIC}' on {BOOTSTRAP_SERVERS}")

    try:
        while True:
            tick = df.sample(1).to_dict(orient="records")[0]
            producer.send(TOPIC, value=tick)
            sleep(INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("Stopping producer")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    main()
