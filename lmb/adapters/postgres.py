import os, shutil, subprocess, tempfile, gzip

from pathlib import Path

from lmb.domain.models import DatabaseConnection


def build_command(pg_dump: str, tables: list[str]) -> list[str]:
    return [
        pg_dump,
        "--no-owner",
        "--no-acl",
        "--no-password",
        "--data-only",
        "--format=plain",
        *(f"--table=public.{table}" for table in tables),
    ]


class PostgresDumper:
    def __init__(self, connection: DatabaseConnection, tables: list[str]) -> None:
        self._connection = connection
        self._tables = tables

    def dump_to(self, destination: Path) -> None:
        pg_dump = shutil.which("pg_dump")
        if pg_dump is None:
            raise RuntimeError("pg_dump is not installed")

        environment = os.environ.copy()
        environment.update(
            {
                "PGHOST": self._connection.host,
                "PGPORT": str(self._connection.port),
                "PGUSER": self._connection.username,
                "PGPASSWORD": self._connection.password,
                "PGDATABASE": self._connection.db_name,
                "PGSSLMODE": self._connection.ssl_mode,
            }
        )
        command = build_command(pg_dump, self._tables)

        with tempfile.TemporaryFile() as stderr_file:
            with subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=stderr_file,
                env=environment,
            ) as process:
                if process.stdout is None:
                    raise RuntimeError("Could not read pg_dump output")
                with gzip.open(destination, "wb") as compressed:
                    shutil.copyfileobj(process.stdout, compressed)
                return_code = process.wait()

            if return_code != 0:
                stderr_file.seek(0)
                detail = stderr_file.read().decode("utf-8", errors="replace")
                raise RuntimeError(f"pg_dump failed: {detail[-4000:]}")
