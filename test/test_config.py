import pytest

from lmb.config import get_tables


class TestGetTables:
    def test_splits_and_strips_names(self, monkeypatch):
        monkeypatch.setenv("BACKUP_TABLES", "work_company, work_skill ,")

        assert get_tables() == ["work_company", "work_skill"]

    def test_requires_variable(self, monkeypatch):
        monkeypatch.delenv("BACKUP_TABLES", raising=False)

        with pytest.raises(KeyError):
            get_tables()

    def test_rejects_empty_list(self, monkeypatch):
        monkeypatch.setenv("BACKUP_TABLES", " , ")

        with pytest.raises(ValueError):
            get_tables()

    def test_rejects_invalid_names(self, monkeypatch):
        monkeypatch.setenv("BACKUP_TABLES", "work_company;DROP TABLE x")

        with pytest.raises(ValueError):
            get_tables()
