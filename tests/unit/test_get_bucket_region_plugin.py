from unittest.mock import Mock
from botocore.model import OperationModel
import logging
from src.s3_region_check_plugin import S3RegionCheckPlugin


def test_check_bucket_region_does_not_log_on_create_bucket(caplog):
    plugin = S3RegionCheckPlugin()
    operation_model = Mock(spec=OperationModel)
    operation_model.name = "CreateBucket"

    with caplog.at_level(logging.INFO):
        plugin.check_bucket_region(operation_model, {"Bucket": "test"})
        assert caplog.text == ""


def test_log_empty_on_operation_without_bucket_input_param(caplog):
    plugin = S3RegionCheckPlugin()
    operation_model = Mock(spec=OperationModel)
    operation_model.name = "ListBuckets"

    with caplog.at_level(logging.INFO):
        plugin.check_bucket_region(operation_model, {})
        assert caplog.text == ""
