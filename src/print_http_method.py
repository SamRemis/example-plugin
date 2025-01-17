import logging
from botocore.client import BaseClient

from botocore.model import OperationModel

logger = logging.getLogger(__name__)


class HttpMethodPlugin:
    # This method will be used to register your custom functionality to a botocore client.
    # Customers will manually call this method to attach the plugin to the clients they
    # create
    def initialize_sample_plugin(self, client: BaseClient) -> None:
        client.meta.events.register("before-call.*.*", self.log_http_method)

    # The arguments that will be passed into this function are controlled by botocore
    # and dependent on the event
    def log_http_method(self, model: OperationModel, **kwargs) -> None:
        logger.info(f"The HTTP method for {model.name} is {model.http['method']}")
