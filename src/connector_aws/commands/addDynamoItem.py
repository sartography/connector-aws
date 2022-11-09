"""AddDynamoItem."""
import json

from connector_aws.auths.simpleAuth import SimpleAuth  # type: ignore

class AddDynamoItem:
    """Add a new record to a dynamo db table."""

    def __init__(self, table_name: str, item_data: dict):
        """
        :param table_name: The name of hte Dynamo DB table to add information to.
        :param item_data: The data to add, should be in json format.
        :return: Json Data structure containing a http status code (hopefully '200' for success..)
            and a response string.
        """
        self.table_name = table_name
        self.fix_floats(item_data)
        self.item_data = item_data

    def execute(self, config, task_data):
        """Execute."""
        # Get the service resource.
        self.dynamodb = SimpleAuth("dynamodb", config).get_resource()
        self.table = self.dynamodb.Table(self.table_name)
        result = self.table.put_item(Item=self.item_data)
        if "ResponseMetadata" in result:
            del result["ResponseMetadata"]
        result_str = json.dumps(result)
        return dict(response=result_str, mimetype="application/json")

    def fix_floats(self, data_dict: dict):
        """Boto3 does not like floats.  It will not accept them.  So we
        identify floats ahead of time and turn them into strings to avoid
        unexpected issues for people.  DynamoDB will correctly interpret
        the number on the other side, as it already knows the types."""
        for key, val in data_dict.items():
            if isinstance(val, float):
                data_dict[key] = str(val)
