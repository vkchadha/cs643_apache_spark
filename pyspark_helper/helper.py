from pyspark.sql import SQLContext
from pyspark.sql import SparkSession


def get_spark_context():
        return  SparkSession \
        .builder \
        .appName("Spark-ML-Model-Training").getOrCreate()

def get_sql_context():
    return SQLContext(get_spark_context())


def read_csv(spark, file_path, delimiter):
    df = spark.read.csv(file_path, sep=delimiter, header=True, inferSchema=True)
    return df


def create_x_y(df, y):
    y = df[y]
    X = df.drop( y)
    return [X, y]