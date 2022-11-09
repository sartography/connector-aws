"""SimpleAuth."""
import boto3  # type: ignore
from botocore.config import Config  # type: ignore


class SimpleAuth:
    """Established a simple Boto 3 Client based on an access key and a secret key."""

    def __init__(self, resource_type: str, config: dict):
        """
        :param access_key: AWS Access Key
        :param secret_key: AWS Secret Key
        """
        aws_access_key_id = config["AWS_ACCESS_KEY_ID"]
        aws_secret_access_key = config["AWS_SECRET_ACCESS_KEY"]
        aws_region = config["AWS_REGION"]

        my_config = Config(
            region_name=aws_region, retries={"max_attempts": 10, "mode": "standard"}
        )

        # Get the service resource.
        self.resource = boto3.resource(
            resource_type,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            config=my_config,
        )

    def get_resource(self):
        """Get_resource."""
        return self.resource
