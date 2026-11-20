from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

from lmb.application.ports import BackupStorage, DatabaseDumper
from lmb.domain.artifact import BackupArtifact


class CreateBackup:
    def __init__(self, dumper: DatabaseDumper, storage: BackupStorage) -> None:
        self._dumper = dumper
        self._storage = storage

    def execute(self, created_at: datetime | None = None) -> BackupArtifact:
        artifact = BackupArtifact.create(
            created_at or datetime.now(timezone.utc),
        )
        with TemporaryDirectory() as work_dir:
            dump_path = Path(work_dir) / "backup.sql.gz"
            self._dumper.dump_to(dump_path)
            self._storage.upload_archive(dump_path, artifact.archive_key)
            self._storage.update_latest(artifact.archive_key, artifact.latest_key)
        return artifact
