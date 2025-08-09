import os


def pytest_sessionstart(session):
    # Enable test-mode harness fallbacks deterministically for tests
    os.environ.setdefault("AIMS_TEST_MODE", "1")
