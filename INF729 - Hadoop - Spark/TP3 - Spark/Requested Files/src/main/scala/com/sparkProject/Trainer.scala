package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.feature.{CountVectorizer, IDF, OneHotEncoder, RegexTokenizer, StopWordsRemover, StringIndexer, VectorAssembler}
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.{Pipeline}
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit, TrainValidationSplitModel}


object Trainer {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12",
      "spark.driver.maxResultSize" -> "2g"
    ))

    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()


    /*******************************************************************************
      *
      *       TP 3
      *
      *       - lire le fichier sauvegarder précédemment
      *       - construire les Stages du pipeline, puis les assembler
      *       - trouver les meilleurs hyperparamètres pour l'entraînement du pipeline avec une grid-search
      *       - Sauvegarder le pipeline entraîné
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/

    println("hello world ! from Trainer")

    // read parquet files
    val fileDataPath = "/home/thelem/TheLEM/Studies/Spark/TP2/TP_ParisTech_2018_2019_starter/TP_ParisTech_2017_2018_starter/data"
    val parquetDF = spark.read.parquet(fileDataPath + "/prepared_trainingset")

    // Pipeline -> First Stage : Creation of tokens
    val tokenizer = new RegexTokenizer()
      .setPattern("\\W+")
      .setGaps(true)
      .setInputCol("text")
      .setOutputCol("tokens")

    // Pipeline -> Second Stage : Removing Stop Words
    val remover = new StopWordsRemover()
      .setInputCol("tokens")
      .setOutputCol("tokens_nsw")

    // Pipeline -> Third Stage : Term Frequency
    val vectorizer = new CountVectorizer()
      .setInputCol("tokens_nsw")
      .setOutputCol("tf")

    // Pipeline -> Fourth Stage : Inverse Document Frequency
    val idf = new IDF()
      .setInputCol("tf")
      .setOutputCol("tfidf")

    // Pipeline -> Fifth Stage : Add Indexer
    val indexer1 = new StringIndexer()
      .setInputCol("country2")
      .setOutputCol("country_indexed")
      .setHandleInvalid("skip")

    // Pipeline -> Sixth Stage : Add Indexer
    val indexer2 = new StringIndexer()
      .setInputCol("currency2")
      .setOutputCol("currency_indexed")
      .setHandleInvalid("skip")

    // Pipeline -> Seventh Stage : One Hot Encoding
    val hotEncoder1 = new OneHotEncoder()
      .setInputCol("country_indexed")
      .setOutputCol("country_onehot")

    // Pipeline -> Eighth Stage : One Hot Encoding
    val hotEncoder2 = new OneHotEncoder()
      .setInputCol("currency_indexed")
      .setOutputCol("currency_onehot")

    // Pipeline -> Ninth Stage : Features for Modeling
    val featuresCreator = new VectorAssembler()
      .setInputCols(Array("tfidf", "days_campaign", "hours_prepa", "goal", "country_onehot", "currency_onehot"))
      .setOutputCol("features")


    // Pipeline -> Tenth Stage : Prediction Model
    val lr = new LogisticRegression()
      .setElasticNetParam(0.0)
      .setFitIntercept(true)
      .setFeaturesCol("features")
      .setLabelCol("final_status")
      .setStandardization(true)
      .setPredictionCol("predictions")
      .setRawPredictionCol("raw_predictions")
      .setThresholds(Array(0.7,0.3))
      .setTol(1.0e-6)
      .setMaxIter(300)

    // Create The Pipeline
    val pipeline = new Pipeline()
      .setStages(Array(tokenizer, remover, vectorizer, idf, indexer1, indexer2, hotEncoder1, hotEncoder2, featuresCreator, lr))

    // Create Training and Test sets
    val Array(training, test) = parquetDF.randomSplit(Array(0.9, 0.1), seed=4500)

    // Parameters Grid
    val paramGrid = new ParamGridBuilder()
      .addGrid(lr.regParam, Array(10e-2, 10e-4, 10e-6, 10e-8))
      .addGrid(vectorizer.minDF, 55.0 to 95.0 by 20.0)
      .build()

    // Train Validation Split
    val evaluator = new MulticlassClassificationEvaluator().setLabelCol("final_status").setPredictionCol("predictions").setMetricName("f1")
    val trainValidationSplit = new TrainValidationSplit()
      .setEstimator(pipeline)
      .setEvaluator(evaluator)
      .setEstimatorParamMaps(paramGrid)
      .setTrainRatio(0.7)

    // Model Creation
    val model = trainValidationSplit.fit(training)


    // Model Testing
    val df_WithPredictions = model.transform(test)
      .select("features", "final_status", "predictions")

    // Score COmputing
    val f1Score = evaluator.evaluate(df_WithPredictions)

    model.write.overwrite().save(fileDataPath + "/model")

    df_WithPredictions.groupBy("final_status", "predictions").count().show()

    println("F1 Score is ===> " + f1Score)

  }
}