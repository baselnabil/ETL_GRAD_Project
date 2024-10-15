from pyspark.sql import SparkSession
from pyspark.sql.types import *



spark = SparkSession.builder \
                .appName('mariadbloader')\
                .getOrCreate()

df = spark.read_csv('./data/raw/salaries_2.csv')

df.to_csv('./data.csv',)