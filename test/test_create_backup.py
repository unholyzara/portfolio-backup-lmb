from datetime import datetime, timezone
from pathlib import Path

from lmb.application.create_backup import CreateBackup


class FakeDumper:
    def __init__(self):
        self.destination = None

    def dump_to(self, destination: Path):
        self.destination = destination
        destination.write_bytes(b"compressed dump")


class FakeStorage:
    def __init__(self):
        self.archive = None
        self.latest = None

    def upload_archive(self, source: Path, key: str):
        self.archive = (source.read_bytes(), key)

    def update_latest(self, archive_key: str, latest_key: str):
        self.latest = (archive_key, latest_key)


class TestCreateBackup:
    def test_uploads_timestamped_archive_and_updates_latest(self):
        dumper = FakeDumper()
        storage = FakeStorage()
        use_case = CreateBackup(dumper, storage)

        artifact = use_case.execute(datetime(2026, 11, 20, 9, 23, tzinfo=timezone.utc))

        expected_key = "api_db-20261120T092300Z.sql.gz"
        assert artifact.archive_key == expected_key
        assert artifact.latest_key == "latest.sql.gz"
        assert storage.archive == (b"compressed dump", expected_key)
        assert storage.latest == (expected_key, "latest.sql.gz")
        assert dumper.destination is not None
        assert not dumper.destination.exists()
