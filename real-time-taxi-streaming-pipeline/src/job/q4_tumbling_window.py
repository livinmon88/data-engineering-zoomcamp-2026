from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

# Streaming environment
env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

# ----------------------------
# Kafka Source Table
# ----------------------------
t_env.execute_sql("""
CREATE TABLE green_trips (
    lpep_pickup_datetime STRING,
    lpep_dropoff_datetime STRING,
    PULocationID INT,
    DOLocationID INT,
    passenger_count DOUBLE,
    trip_distance DOUBLE,
    tip_amount DOUBLE,
    total_amount DOUBLE,

    event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
    WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'green-trips',
    'properties.bootstrap.servers' = 'redpanda:29092',
    'properties.group.id' = 'flink-green',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true'
)
""")

# ----------------------------
# PostgreSQL Sink Table
# ----------------------------
t_env.execute_sql("""
CREATE TABLE pickup_counts (
    window_start TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT,
    PRIMARY KEY (window_start, PULocationID) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/postgres',
    'table-name' = 'pickup_counts',
    'username' = 'postgres',
    'password' = 'postgres',
    'driver' = 'org.postgresql.Driver'
)
""")

# ----------------------------
# Tumbling Window Aggregation
# ----------------------------
t_env.execute_sql("""
INSERT INTO pickup_counts
SELECT
    window_start,
    PULocationID,
    COUNT(*) AS num_trips
FROM TABLE(
    TUMBLE(TABLE green_trips, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTES)
)
GROUP BY window_start, PULocationID
""").wait()