from unittest.mock import Mock
from botocore.model import OperationModel
import logging
from src.print_http_method import HttpMethodPlugin


def test_log_http_method(caplog):
    plugin = HttpMethodPlugin()

    operation_model = Mock(spec=OperationModel)
    operation_model.name = "TestOperation"
    operation_model.http = {"method": "GET"}

    with caplog.at_level(logging.INFO):
        plugin.log_http_method(operation_model)

    assert "The HTTP method for TestOperation is GET" in caplog.text
