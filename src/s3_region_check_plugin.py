from functools import lru_cache

import botocore.session
from botocore import client

import logging

logger = logging.getLogger(__name__)


class S3RegionCheckPlugin:
    def __init__(self):
        session = botocore.session.get_session()
        self._s3_client = session.create_client('s3')

    def initialize_sample_plugin(self, client: client.BaseClient) -> None:
        self._client_region = client.meta.region_name
        client.meta.events.register('provide-client-params.s3.*', self.check_bucket_region)

    def check_bucket_region(self, model, params, **kwargs) -> None:
        # We can't call get the region of a bucket that doesn't exist yet
        if model.name == 'CreateBucket':
            return
        elif bucket := params.get('Bucket'):
            bucket_region = self._get_bucket_region(bucket)
            if bucket_region != self._client_region:
                logger.warning(f"The client is configured to use "
                               f"{self._client_region}, but {bucket} is in {bucket_region}")
            else:
                logger.info(f"Client is configured to use the correct region")

    #This #lru_cache annotation is using python's functools package; on subsequent
    # calls with the same input, it will return the value from the cache instead of
    # calling the service.  See here for more info: https://docs.python.org/3/library/functools.html
    @lru_cache(maxsize=100)
    def _get_bucket_region(self, bucket) -> str:
        return self._s3_client.head_bucket(Bucket=bucket)['BucketRegion']
