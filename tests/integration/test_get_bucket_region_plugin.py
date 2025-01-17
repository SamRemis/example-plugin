import logging
import uuid
import pytest
from botocore.session import get_session
from src.s3_region_check_plugin import S3RegionCheckPlugin


@pytest.fixture(scope="module")
def s3_client_us_west_2():
    session = get_session()
    client = session.create_client("s3", region_name="us-west-2")
    plugin = S3RegionCheckPlugin()
    plugin.initialize_sample_plugin(client)
    return client


@pytest.fixture(scope="module")
def s3_client_us_east_2():
    session = get_session()
    client = session.create_client("s3", region_name="us-east-2")
    plugin = S3RegionCheckPlugin()
    plugin.initialize_sample_plugin(client)
    return client


@pytest.fixture(scope="module")
def s3_bucket_us_west_2(s3_client_us_west_2):
    bucket_name = f"test-bucket-{uuid.uuid4()}"
    s3_client_us_west_2.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={"LocationConstraint": "us-west-2"},
    )
    yield bucket_name
    s3_client_us_west_2.delete_bucket(Bucket=bucket_name)


def test_check_bucket_region_correct_region(
    caplog, s3_client_us_west_2, s3_bucket_us_west_2
):
    plugin = S3RegionCheckPlugin()
    plugin.initialize_sample_plugin(s3_client_us_west_2)
    with caplog.at_level(logging.INFO):
        s3_client_us_west_2.list_objects_v2(Bucket=s3_bucket_us_west_2)
        assert "Client is configured to use the correct region" in caplog.text


def test_check_bucket_region_incorrect_region(
    caplog, s3_client_us_east_2, s3_bucket_us_west_2
):
    plugin = S3RegionCheckPlugin()
    plugin.initialize_sample_plugin(s3_client_us_east_2)
    with caplog.at_level(logging.WARN):
        s3_client_us_east_2.list_objects_v2(Bucket=s3_bucket_us_west_2)
        assert "The client is configured to use us-east-2, but " in caplog.text
