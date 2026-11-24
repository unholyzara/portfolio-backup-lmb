from dataclasses import dataclass

@dataclass
class Secrets:
    username: str
    password: str
    db_name: str

@dataclass
class DatabaseConnection:
    host: str
    username: str
    password: str
    db_name: str
    port: int
    ssl_mode = "require"
