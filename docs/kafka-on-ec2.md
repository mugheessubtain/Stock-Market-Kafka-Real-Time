# Running Kafka on Amazon EC2

Step-by-step setup for a single-broker Kafka 3.3.1 cluster on an Amazon Linux EC2 instance.

## 1. Install Java and Kafka

```bash
sudo yum install java-1.8.0-openjdk
java -version

wget https://archive.apache.org/dist/kafka/3.3.1/kafka_2.12-3.3.1.tgz
tar -xvf kafka_2.12-3.3.1.tgz
cd kafka_2.12-3.3.1
```

## 2. Start ZooKeeper

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
```

## 3. Start the Kafka broker

Open a second SSH session to the instance. On small instances, limit the heap first:

```bash
export KAFKA_HEAP_OPTS="-Xmx256M -Xms128M"
cd kafka_2.12-3.3.1
bin/kafka-server-start.sh config/server.properties
```

By default the broker advertises the instance's private address. To reach it from outside the VPC, edit `config/server.properties` and set `advertised.listeners` to the instance's public IP:

```properties
advertised.listeners=PLAINTEXT://<EC2_PUBLIC_IP>:9092
```

Also allow inbound traffic on port `9092` in the instance's security group.

## 4. Create the topic

```bash
bin/kafka-topics.sh --create --topic demo_test \
  --bootstrap-server <EC2_PUBLIC_IP>:9092 \
  --replication-factor 1 --partitions 1
```

## 5. Smoke-test with the console clients

```bash
# producer
bin/kafka-console-producer.sh --topic demo_test --bootstrap-server <EC2_PUBLIC_IP>:9092

# consumer, in another session
bin/kafka-console-consumer.sh --topic demo_test --bootstrap-server <EC2_PUBLIC_IP>:9092
```

Messages typed into the producer should appear in the consumer. You're ready to run `src/producer.py` and `src/consumer.py`.
