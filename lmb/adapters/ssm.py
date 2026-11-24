from dataclasses import dataclass

import boto3

from lmb.domain.models import Secrets, DatabaseConnection


@dataclass
class SSMClient:
    aws_region: str

    def __post_init__(self):
        session = boto3.Session()
        self.client = session.client("ssm", region_name=self.aws_region)

    def get_secret_value(self, parameter: str) -> str:
        response = self.client.get_parameter(
            Name=parameter, WithDecryption=True
        )
        value = response.get("Parameter", {}).get("Value")
        if not isinstance(value, str):
            raise ValueError("SSM parameter must contain a string value")
        return value


def get_secrets(
    db_user_param: str,
    db_password_param: str,
    db_name_param: str,
    ssm: SSMClient,
):
    db_user = ssm.get_secret_value(parameter=db_user_param)
    db_password = ssm.get_secret_value(parameter=db_password_param)
    db_name = ssm.get_secret_value(parameter=db_name_param)
    return Secrets(username=db_user, password=db_password, db_name=db_name)


def load_database_connection(
    secrets: Secrets, db_host: str, db_port: int
) -> DatabaseConnection:
    return DatabaseConnection(
        host=db_host,
        username=secrets.username,
        password=secrets.password,
        db_name=secrets.db_name,
        port=db_port,
    )
