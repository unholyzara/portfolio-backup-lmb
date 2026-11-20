import json

from typing import Any
from dataclasses import dataclass

import boto3

from lmb.domain.models import DatabaseConnection


@dataclass
class SecretManagerClient:
    secret_name: str
    aws_region: str

    def __post_init__(self):
        session = boto3.Session()
        self.client = session.client("secretmanager", region_name=self.aws_region)

    def get_secrets(self) -> dict[str, Any]:
        response = self.client.get_secret_value(SecretId=self.secret_name)
        secret_string = response.get("SecretString")
        if not isinstance(secret_string, str):
            raise ValueError("Database secret must contain a SecretString")

        secret = json.loads(secret_string)
        if not isinstance(secret, dict):
            raise ValueError("Database secret must be a JSON object")
        return secret


def load_database_connection(
    secrets: dict[str, Any], db_host: str, db_user: str, db_name: str, db_port: int
) -> DatabaseConnection:
    return DatabaseConnection(
        host=db_host,
        username=db_user,
        password=secrets["DB_PASSWORD"],
        db_name=db_name,
        port=db_port,
    )
