import pytest
import json


def pytest_addoption(parser):
    parser.addoption("--test_data", action="store", default=None)


@pytest.fixture
def test_data(request):
    data_str = request.config.getoption("--test_data")
    if data_str is None:
        pytest.skip("No test data provided")
    return json.loads(data_str)
