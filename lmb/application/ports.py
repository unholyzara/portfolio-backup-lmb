from pathlib import Path
from typing import Protocol


class DatabaseDumper(Protocol):
    def dump_to(self, destination: Path) -> None: ...


class BackupStorage(Protocol):
    def upload_archive(self, source: Path, key: str) -> None: ...

    def update_latest(self, archive_key: str, latest_key: str) -> None: ...
