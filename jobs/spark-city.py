from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, DoubleType, IntegerType, StringType, TimestampType, FloatType

from jobs.config import configuration
from pyspark.sql.functions import col, from_json


# SmartCityStreaming anune poxel
def main():
    spark = SparkSession.builder.appName("Streaming") \
        .config("spark.jars.packages",
                "org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0,"
                "org.apache.hadoop:hadoop-aws:3.3.1,"
                "com.amazonaws:aws-java-sdk:1.11.469") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.access.key", configuration.get('AWS_ACCESS_KEY')) \
        .config("spark.hadoop.fs.s3a.secret.key", configuration.get('AWS_SECRET_KEY')) \
        .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider') \
        .getOrCreate()

    # Adjust the log level to minimize the console output on executor
    spark.sparkContext.setLogLevel('INFO')

    weather_schema = StructType([
        StructField('lon', DoubleType(), True),
        StructField('lat', DoubleType(), True),
        StructField('weather_id', IntegerType(), True),
        StructField('main', StringType(), True),
        StructField('description', StringType(), True),
        StructField('icon', StringType(), True),
        StructField('temp', DoubleType(), True),
        StructField('feels_like', DoubleType(), True),
        StructField('temp_min', DoubleType(), True),
        StructField('temp_max', DoubleType(), True),
        StructField('pressure', IntegerType(), True),
        StructField('humidity', IntegerType(), True),
        StructField('visibility', IntegerType(), True),
        StructField('wind_speed', DoubleType(), True),
        StructField('wind_deg', IntegerType(), True),
        StructField('clouds_all', IntegerType(), True),
        StructField('country', StringType(), True),
        StructField('sunrise', TimestampType(), True),
        StructField('sunset', TimestampType(), True),
        StructField('timezone', IntegerType(), True),
        StructField('city_id', IntegerType(), True),
        StructField('city_name', StringType(), True),
        StructField('cod', IntegerType(), True)
    ])

    air_quality_schema = StructType([
        StructField("status", StringType(), True),
        StructField("aqi", StringType(), True),
        StructField("idx", StringType(), True),
        StructField("attribution1_url", StringType(), True),
        StructField("attribution1_name", StringType(), True),
        StructField("attribution2_url", StringType(), True),
        StructField("attribution2_name", StringType(), True),
        StructField("city_geo_lat", FloatType(), True),
        StructField("city_geo_lon", FloatType(), True),
        StructField("city_name", StringType(), True),
        StructField("city_url", StringType(), True),
        StructField("dew_value", FloatType(), True),
        StructField("h_value", FloatType(), True),
        StructField("no2_value", FloatType(), True),
        StructField("so2_value", FloatType(), True),
        StructField("o3_value", FloatType(), True),
        StructField("p_value", FloatType(), True),
        StructField("pm10_value", FloatType(), True),
        StructField("pm25_value", FloatType(), True),
        StructField("t_value", FloatType(), True),
        StructField("w_value", FloatType(), True),
        StructField("wg_value", FloatType(), True),
        StructField("time_s", StringType(), True),
        StructField("time_tz", StringType(), True),
        StructField("time_v", StringType(), True),
        StructField("time_iso", StringType(), True),
        StructField("debug_sync", StringType(), True)
    ])

    def read_kafka_topic(topic, schema):
        return (spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', 'broker:29092')
                .option('subscribe', topic)
                .option('startingOffsets', 'earliest')
                .load()
                .selectExpr("CAST(value AS STRING)")
                .select(from_json(col('value'), schema).alias('data'))
                .select('data.*')
                )

    def stream_writer(data_frame: DataFrame, checkpointFolder, output):
        return (data_frame.writeStream
                .format('parquet')
                .option('checkpointLocation', checkpointFolder)
                .option('path', output)
                .outputMode('append')
                .start())

    weather_df = read_kafka_topic('weather_data', weather_schema).alias('weather')
    quality_df = read_kafka_topic('quality_data', air_quality_schema).alias('quality')

    query1 = stream_writer(weather_df, 's3a://goodair/checkpoints/weather_data',
                           's3a://goodair/data/weather_data')

    query2 = stream_writer(quality_df, 's3a://goodair/checkpoints/quality_data',
                           's3a://goodair/data/quality_data')

    query2.awaitTermination()


if __name__ == "__main__":
    main()
