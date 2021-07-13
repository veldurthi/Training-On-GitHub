# Databricks notebook source


# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC ls /databricks/init_scripts/

# COMMAND ----------

dbutils.widgets.dropdown("X123", "1", [str(x) for x in range(1, 10)])

# COMMAND ----------

blob_account_name = "azureopendatastorage"
blob_container_name = "citydatacontainer"
blob_relative_path = "Safety/Release/city=Seattle"
blob_sas_token = r"?st=2019-02-26T02%3A34%3A32Z&se=2119-02-27T02%3A34%3A00Z&sp=rl&sv=2018-03-28&sr=c&sig=XlJVWA7fMXCSxCKqJm8psMOh0W4h7cSYO28coRqF2fs%3D"

# COMMAND ----------

wasbs_path = 'wasbs://%s@%s.blob.core.windows.net/%s' % (blob_container_name, blob_account_name, blob_relative_path)
spark.conf.set('fs.azure.sas.%s.%s.blob.core.windows.net' % (blob_container_name, blob_account_name), blob_sas_token)
print('Remote blob path: ' + wasbs_path)

# COMMAND ----------

df = spark.read.parquet(wasbs_path)
print('Register the DataFrame as a SQL temporary view: source')
df.createOrReplaceTempView('source')

# COMMAND ----------

print('Displaying top 10 rows: ')9
display(spark.sql('SELECT * FROM source LIMIT 10'))