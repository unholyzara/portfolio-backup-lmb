from lmb.adapters.postgres import build_command


class TestBuildCommand:
    def test_dumps_only_data_of_listed_tables(self):
        command = build_command("pg_dump", ["work_company", "work_skill"])

        assert command[0] == "pg_dump"
        assert "--data-only" in command
        assert "--table=public.work_company" in command
        assert "--table=public.work_skill" in command
        assert not any(arg.startswith("--exclude") for arg in command)
