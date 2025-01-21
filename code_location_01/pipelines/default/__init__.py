from dagster import Definitions, EnvVar, schedule
from dagster_aws.s3 import S3PickleIOManager, S3Resource
from dagster_docker import docker_executor

from .assets.asset_default import asset_default
from .job.etl_pipeline import etl_op_graph
from .resource.sql_alchemy import SqlAlchemyClientResource

etl_pipeline = etl_op_graph.to_job(name="etl_pipeline_default", executor_def=docker_executor)


@schedule(cron_schedule="*/5 * * * *", job=etl_pipeline)
def schedule_etl(_context):
    return {}


defs = Definitions(
    assets=[asset_default],
    resources={
        "io_manager": S3PickleIOManager(
            s3_resource=S3Resource(
                aws_access_key_id=EnvVar("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=EnvVar("AWS_SECRET_ACCESS_KEY"),
            ),
            s3_bucket="etl-dagster-data",
            s3_prefix="op-io-data",
        ),
        "s3_io_manager": S3Resource(
            aws_access_key_id=EnvVar("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=EnvVar("AWS_SECRET_ACCESS_KEY"),
        ),
        "postgres_io_manager": SqlAlchemyClientResource(
            database_ip=EnvVar("DATABASE_IP"),
            database_port=EnvVar("DATABASE_PORT"),
            database_user=EnvVar("DATABASE_USER"),
            database_password=EnvVar("DATABASE_PASSWORD"),
            database_name=EnvVar("DATABASE_NAME"),
        ),
    },
    schedules=[schedule_etl],
)
