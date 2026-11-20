import os


def get_aws_region():
    return os.environ["AWS_REGION"]


def get_bucket():
    return os.environ["BACKUP_BUCKET"]


def get_secret_name():
    return os.environ["SECRET_NAME"]


def get_db_host():
    return os.environ["DB_HOST"]


def get_db_user():
    return os.environ["DB_USER"]


def get_db_name():
    return os.environ["DB_NAME"]


def get_db_port():
    return int(os.environ["DB_PORT"])
