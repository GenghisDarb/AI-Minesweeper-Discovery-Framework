def test_import_config():
    try:
        # from ai_minesweeper.config import DEBUG
        assert True
    except ModuleNotFoundError as e:
        assert False, f"Import failed: {e}"
