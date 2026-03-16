from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)

settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
t_env = StreamTableEnvironment.create(env, environment_settings=settings)

# Kafka source
t_env.execute_sql("""
CREATE TABLE green_trips (
    lpep_pickup_datetime STRING,
    PULocationID INT,

    event_timestamp AS TO_TIMESTAMP(lpep_pickup_datetime, 'yyyy-MM-dd HH:mm:ss'),
    WATERMARK FOR event_timestamp AS event_timestamp - INTERVAL '5' SECOND
) WITH (
    'connector' = 'kafka',
    'topic' = 'green-trips',
    'properties.bootstrap.servers' = 'redpanda:29092',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'json',
    'json.ignore-parse-errors' = 'true'
)
""")

# Postgres sink
t_env.execute_sql("""
CREATE TABLE session_counts (
    session_start TIMESTAMP(3),
    session_end TIMESTAMP(3),
    PULocationID INT,
    num_trips BIGINT,
    PRIMARY KEY (session_start, session_end, PULocationID) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/postgres',
    'table-name' = 'session_counts',
    'username' = 'postgres',
    'password' = 'postgres',
    'driver' = 'org.postgresql.Driver'
)
""")

# Session window
t_env.execute_sql("""
INSERT INTO session_counts
SELECT
    window_start,
    window_end,
    PULocationID,
    COUNT(*) AS num_trips
FROM TABLE(
    SESSION(TABLE green_trips, DESCRIPTOR(event_timestamp), INTERVAL '5' MINUTES)
)
GROUP BY window_start, window_end, PULocationID
""").wait()