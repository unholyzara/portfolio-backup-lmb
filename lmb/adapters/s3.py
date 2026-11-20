from pathlib import Path

import boto3


class S3BackupStorage:
    def __init__(self, bucket: str) -> None:
        self._client = boto3.client("s3")
        self._bucket = bucket

    def upload_archive(self, source: Path, key: str) -> None:
        self._client.upload_file(
            str(source),
            self._bucket,
            key,
            ExtraArgs={"ContentType": "application/gzip"},
        )

    def update_latest(self, archive_key: str, latest_key: str) -> None:
        self._client.copy_object(
            Bucket=self._bucket,
            Key=latest_key,
            CopySource={"Bucket": self._bucket, "Key": archive_key},
            MetadataDirective="COPY",
        )
