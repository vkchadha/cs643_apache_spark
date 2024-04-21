from pyspark_helper.helper import get_spark_context , read_csv
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml import PipelineModel

spark = get_spark_context()
valid_file_name = "/app/data/ValidationDataset.csv"
spark_train_df = read_csv(spark, valid_file_name, delimiter=";")
pipelineModel = PipelineModel.load("/app/model/pyspark_log_reg.ml")
predictionsDF = pipelineModel.transform(spark_train_df)
predictionsDF.show()

prediction = pipelineModel.transform(spark_train_df)
ml_output = prediction.select("features",  "quality", "prediction")
#
evaluator = MulticlassClassificationEvaluator(labelCol='quality', predictionCol="prediction")
acc = evaluator.evaluate(ml_output, {evaluator.metricName: "accuracy"})
f1 = evaluator.evaluate(ml_output, {evaluator.metricName: "f1"})
weightedPrecision = evaluator.evaluate(ml_output, {evaluator.metricName: "weightedPrecision"})
weightedRecall = evaluator.evaluate(ml_output, {evaluator.metricName: "weightedRecall"})
auc = evaluator.evaluate(ml_output)
#
print(f'ML Reader output {acc}')
print(f'f1 score {f1} :')
print(f'weightedPrecision score {weightedPrecision} :')
print(f'weightedRecall score {weightedRecall} :')
print(f'auc score {auc} :')
# #
