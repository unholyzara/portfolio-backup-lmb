from datetime import datetime

import pytest

from lmb.domain.artifact import BackupArtifact


class TestBackupArtifact:
    def test_normalizes_scheduled_time_to_utc(self):
        artifact = BackupArtifact.create(
            datetime.fromisoformat("2026-11-20T10:23:00+01:00"),
        )

        assert artifact.archive_key == "api_db-20261120T092300Z.sql.gz"

    def test_rejects_timezone_naive_time(self):
        with pytest.raises(ValueError, match="timezone"):
            BackupArtifact.create(datetime(2026, 11, 20, 9, 23))
