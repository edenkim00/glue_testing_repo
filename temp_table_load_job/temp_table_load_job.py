import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame
from awsglue.dynamicframe import DynamicFrame

print("HIHI")
def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1706582320391 = glueContext.create_dynamic_frame.from_catalog(
    database="processed_raw_events",
    table_name="notifly_event_logs",
    transformation_ctx="AWSGlueDataCatalog_node1706582320391",
)

# Script generated for node SQL Query
SqlQuery57 = """
select project_id, name, notifly_user_id, time, dt from myDataSource where project_id='a0d696d1aba7535fad6710cddf3b1cab' and dt>='2024-01-31'
"""
SQLQuery_node1706582335076 = sparkSqlQuery(
    glueContext,
    query=SqlQuery57,
    mapping={"myDataSource": AWSGlueDataCatalog_node1706582320391},
    transformation_ctx="SQLQuery_node1706582335076",
)

# RDS PostgreSQL 연결 정보 설정
connection_options = {
    "url": "jdbc:postgresql://notifly-rds-proxy.proxy-cwvdx2o498bl.ap-northeast-2.rds.amazonaws.com:5432/postgres",
    "dbtable": "temp",
    "database": "postgres",
    "user": "postgres",
    "password": "X80428v5h9l1QwuACZoV",
}

# DynamicFrame을 PostgreSQL 테이블에 적재
glueContext.write_dynamic_frame.from_jdbc_conf(
    frame=SQLQuery_node1706582335076,  # 이 부분을 수정하여 SQL Query 결과를 사용
    catalog_connection="Postgresql connection",
    connection_options=connection_options
)

job.commit()
