import os


def get_aws_region():
    return os.environ["AWS_REGION"]


def get_bucket():
    return os.environ["BACKUP_BUCKET"]


def get_secret_name():
    return os.environ["SECRET_NAME"]


def get_db_host():
    return os.environ["DB_HOST"]


def get_db_user_param():
    return os.environ["DB_USER_SMM"]

def get_db_password_param():
    return os.environ["DB_PASSWORD_SMM"]

def get_db_name_param():
    return os.environ["DB_NAME_SMM"]


def get_db_port():
    return int(os.environ["DB_PORT"])
