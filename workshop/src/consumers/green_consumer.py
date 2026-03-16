import json
from kafka import KafkaConsumer

TOPIC = "green-trips"

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

count = 0

# Poll messages in batches (much faster)
while True:
    records = consumer.poll(timeout_ms=1000)

    if not records:
        break

    for tp, messages in records.items():
        for message in messages:
            trip = message.value
            if trip["trip_distance"] and trip["trip_distance"] > 5:
                count += 1

print("Trips with distance > 5 km:", count)

consumer.close()