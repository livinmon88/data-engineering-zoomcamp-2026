# 🚕 Real-Time Streaming Pipeline with Kafka, PyFlink, and PostgreSQL

This project demonstrates a **real-time data streaming pipeline** built using **Redpanda (Kafka-compatible broker), Apache Flink (PyFlink), and PostgreSQL**.

The pipeline processes **NYC Green Taxi Trip data** and performs **stream processing using window aggregations**.

This project was developed as part of the **Data Engineering Zoomcamp Streaming Homework**.

---

# 🏗 Architecture

Producer → Kafka (Redpanda) → Apache Flink → PostgreSQL

```
Green Taxi Dataset
        │
        ▼
 Python Producer
        │
        ▼
 Redpanda (Kafka Topic)
        │
        ▼
 Apache Flink Streaming Jobs
        │
        ▼
 PostgreSQL (Analytics Tables)
```

---

# 📂 Project Structure

```
workshop/
│
├── docker-compose.yml
├── Dockerfile.flink
├── flink-config.yaml
│
├── src/
│   ├── producers/
│   │   ├── producer.py
│   │   ├── producer_realtime.py
│   │   └── green_producer.py
│   │
│   ├── consumers/
│   │   ├── consumer.py
│   │   └── consumer_postgres.py
│   │
│   └── job/
│       ├── pass_through_job.py
│       ├── q4_tumbling_window.py
│       ├── q5_session_window.py
│       └── q6_tip_window.py
```

---

# ⚙️ Technologies Used

| Tool         | Purpose                         |
| ------------ | ------------------------------- |
| Docker       | Container orchestration         |
| Redpanda     | Kafka-compatible message broker |
| Apache Flink | Stream processing               |
| PyFlink      | Python API for Flink            |
| PostgreSQL   | Storage for processed results   |
| Python       | Producer and streaming jobs     |

---

# 🚀 Setup Instructions

### 1️⃣ Start Infrastructure

```
docker compose build
docker compose up -d
```

Services started:

* Redpanda (Kafka broker)
* Apache Flink JobManager
* Apache Flink TaskManager
* PostgreSQL

Flink UI:

```
http://localhost:8081
```

---

# 📡 Data Ingestion

Taxi trip data is read from:

```
green_tripdata_2025-10.parquet
```

Producer sends records to the Kafka topic:

```
green-trips
```

Run the producer:

```
uv run python src/producers/green_producer.py
```

# 📊 Key Stream Processing Concepts

This project demonstrates:

* Kafka streaming ingestion
* Event time processing
* Watermarks
* Tumbling windows
* Session windows
* Flink SQL streaming
* JDBC sink to PostgreSQL

---

# 🧠 Learning Outcomes

By completing this project, I learned how to:

* Build a **real-time streaming pipeline**
* Use **Kafka / Redpanda as a message broker**
* Implement **window aggregations in Apache Flink**
* Handle **event-time processing and watermarks**
* Persist streaming results into **PostgreSQL**

---

# 📚 References

* Data Engineering Zoomcamp
* Apache Flink Documentation
* Redpanda Streaming Platform
* NYC Taxi Dataset

---

# 👨‍💻 Author

Livin Vincent

Data Engineering Zoomcamp 2026
