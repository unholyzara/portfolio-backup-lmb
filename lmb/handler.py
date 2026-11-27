from datetime import datetime, timezone
from typing import Any, Mapping

from lmb.config import (
    get_aws_region,
    get_bucket,
    get_db_host,
    get_db_port,
    get_db_user_param,
    get_db_password_param,
    get_db_name_param,
    get_tables,
)
from lmb.adapters.postgres import PostgresDumper
from lmb.adapters.s3 import S3BackupStorage
from lmb.adapters.ssm import SSMClient, get_secrets, load_database_connection
from lmb.application.create_backup import CreateBackup


def _scheduled_time(event: Mapping[str, Any]) -> datetime:
    value = event.get("scheduledTime") or event.get("time")
    if value is None:
        return datetime.now(timezone.utc)
    if not isinstance(value, str):
        raise ValueError("scheduledTime must be an ISO-8601 string")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def handler(event: Mapping[str, Any], context: Any) -> dict[str, str]:

    bucket = get_bucket()
    aws_region = get_aws_region()

    ssm_client = SSMClient(aws_region=aws_region)

    secrets = get_secrets(
        db_user_param=get_db_user_param(),
        db_password_param=get_db_password_param(),
        db_name_param=get_db_name_param(),
        ssm=ssm_client,
    )

    connection = load_database_connection(
        secrets=secrets, db_host=get_db_host(), db_port=get_db_port()
    )
    use_case = CreateBackup(
        dumper=PostgresDumper(connection=connection, tables=get_tables()),
        storage=S3BackupStorage(bucket=bucket),
    )
    artifact = use_case.execute(created_at=_scheduled_time(event))
    return {
        "bucket": bucket,
        "archiveKey": artifact.archive_key,
        "latestKey": artifact.latest_key,
    }
