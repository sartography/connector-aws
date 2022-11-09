"""ScanDynamoTable."""
import simplejson as json

from connector_aws.auths.simpleAuth import SimpleAuth  # type: ignore


class ScanDynamoTable:
    """Return all records in a given table.  Potentially very expensive."""

    def __init__(self, table_name: str):
        """
        :param table_name: The name of hte Dynamo DB table to scan
        :return: Json Data structure containing the requested data.
        """
        self.table_name = table_name

    def execute(self, config, task_data):
        """Execute."""
        dynamodb = SimpleAuth("dynamodb", config).get_resource()
        table = dynamodb.Table(self.table_name)
        result = table.scan()
        if "ResponseMetadata" in result:
            del result["ResponseMetadata"]
        result_str = json.dumps(result, use_decimal=True)
        return dict(response=result_str, mimetype="application/json")
