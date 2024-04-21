
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler
import pandas as pd
import numpy as np
from pyspark.ml.evaluation import MulticlassClassificationEvaluator


def get_spark_context():
    return SparkSession \
        .builder \
        .appName("Spark-ML-Model-Training").getOrCreate()


def get_sql_context():
    return SQLContext(get_spark_context())


def read_csv(spark, file_path, delimiter):
    df = spark.read.csv(file_path, sep=delimiter, header=True, inferSchema=True)
    return df


def create_test_train_df(df, threshold):
    msk = np.random.rand(len(df)) < threshold
    spark_train_df = spark.createDataFrame(df[msk])
    spark_test_df = spark.createDataFrame(df[~msk])

    return spark_train_df, spark_test_df


def get_results(ml_output):

    evaluator = MulticlassClassificationEvaluator(labelCol='quality', predictionCol="prediction")
    results_dict = {
        'acc': evaluator.evaluate(ml_output, {evaluator.metricName: "accuracy"}),
        'f1': evaluator.evaluate(ml_output, {evaluator.metricName: "f1"}),
        'weightedPrecision': evaluator.evaluate(ml_output, {evaluator.metricName: "weightedPrecision"}),
        'weightedRecall': evaluator.evaluate(ml_output, {evaluator.metricName: "weightedRecall"}),
        'auc': evaluator.evaluate(ml_output)
    }
    return results_dict


spark = get_spark_context()
train_file_name = "s3://vc35sparktraining/TrainingDataset.csv"
#train_file_name  ="data/TrainingDataset.csv"
#valid_file_name = "s3://vc35sparktraining/ValidationDataset.csv"
df = pd.read_csv(train_file_name, sep=";")
spark_train_df, spark_test_df = create_test_train_df(pd.read_csv(train_file_name, sep=";"), 0.8)

features = ["fixed acidity","volatile acidity","citric acid"
            ,"residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide"
            ,"density","pH","sulphates","alcohol"]

vectorAssembler = VectorAssembler().setInputCols(features).setOutputCol("features")
lr = LogisticRegression(maxIter=10, regParam=0.001).setFeaturesCol("features").setLabelCol("quality")
stages = [vectorAssembler, lr]
pipeline = Pipeline(stages=stages)
model = pipeline.fit(spark_train_df)

prediction = model.transform(spark_test_df)
ml_output = prediction.select("features",  "quality", "prediction")
results_dict = get_results(ml_output)

print(f'ML Reader output {results_dict["acc"]}')
print(f'f1 score : {results_dict["f1"]}')
print(f'weightedPrecision score : {results_dict["weightedPrecision"]}')
print(f'weightedRecall score : {results_dict["weightedRecall"]} ')
print(f'auc score {results_dict["auc"]} :')

results_df = pd.DataFrame.from_dict(results_dict, orient = 'index')
results_df.to_csv(r's3://vc35sparktraining/model/results/model_results.text', header=None, index=True, sep=' ', mode='w')
model.write().overwrite().save("s3://vc35sparktraining/model/pyspark_log_reg.ml")

