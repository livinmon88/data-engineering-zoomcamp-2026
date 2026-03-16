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
    tip_amount DOUBLE,

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

# PostgreSQL sink
t_env.execute_sql("""
CREATE TABLE tip_hourly (
    window_start TIMESTAMP(3),
    total_tip DOUBLE,
    PRIMARY KEY (window_start) NOT ENFORCED
) WITH (
    'connector' = 'jdbc',
    'url' = 'jdbc:postgresql://postgres:5432/postgres',
    'table-name' = 'tip_hourly',
    'username' = 'postgres',
    'password' = 'postgres',
    'driver' = 'org.postgresql.Driver'
)
""")

# 1-hour tumbling window
t_env.execute_sql("""
INSERT INTO tip_hourly
SELECT
    window_start,
    SUM(tip_amount) AS total_tip
FROM TABLE(
    TUMBLE(TABLE green_trips, DESCRIPTOR(event_timestamp), INTERVAL '1' HOUR)
)
GROUP BY window_start
""").wait()