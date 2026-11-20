from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class BackupArtifact:
    created_at: datetime
    archive_key: str
    latest_key: str

    @classmethod
    def create(cls, created_at: datetime) -> "BackupArtifact":
        if created_at.tzinfo is None:
            raise ValueError("created_at must include a timezone")

        utc_time = created_at.astimezone(timezone.utc)
        timestamp = utc_time.strftime("%Y%m%dT%H%M%SZ")
        return cls(
            created_at=utc_time,
            archive_key=f"api_db-{timestamp}.sql.gz",
            latest_key=f"latest.sql.gz",
        )
