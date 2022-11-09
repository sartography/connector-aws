"""QueryDynamoTable."""
import simplejson as json
from boto3.dynamodb.conditions import Key
from connector_aws.auths.simpleAuth import SimpleAuth  # type: ignore


class QueryDynamoTable:
    """Return all records for a given partition key, and optionally a sort_key."""

    def __init__(self, table_name: str, partition_key: str, sort_key: str = None):
        """
        :param table_name: The name of hte Dynamo DB table to add information to.
        :param partition_key: The value to search for in the partition key
        :param sort_key: The value to search for in the sork_key (optional)
        :return: Json Data structure containing the requested data.
        """
        self.table_name = table_name
        self.partition_key = partition_key
        self.sort_key = sort_key

    def execute(self, config, task_data):
        """Execute."""
        dynamodb = SimpleAuth("dynamodb", config).get_resource()
        table = dynamodb.Table(self.table_name)
        partition_key_name = self.get_schema_key_name(table, "HASH")
        sort_key_name = self.get_schema_key_name(table, "RANGE")
        query = {partition_key_name: self.partition_key}
        condition = Key(partition_key_name).eq(self.partition_key)
        if self.sort_key:
            condition = condition & Key(sort_key_name).eq(self.sort_key)
        result = table.query(KeyConditionExpression=condition)
        if "ResponseMetadata" in result:
            del result["ResponseMetadata"]
        result_str = json.dumps(result)
        return dict(response=result_str, mimetype="application/json")

    def get_schema_key_name(self, table, key_type: str):
        """Get_schema_key_name."""
        for item in table.key_schema:
            if item["KeyType"] == key_type:
                return item["AttributeName"]
