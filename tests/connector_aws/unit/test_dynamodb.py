import simplejson as json

from moto import mock_dynamodb
import boto3

MY_CONFIG = {"AWS_ACCESS_KEY_ID": "1234", "AWS_SECRET_ACCESS_KEY": "4567", "AWS_REGION": "us-east-1"}


def create_movie_table(dynamodb=None):
    """A little helper function to make testing easier.  Creates a Movies table with year and title columns."""
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )


def add_sample_records():
    from connector_aws.commands.addDynamoItem import AddDynamoItem
    AddDynamoItem('Movies', {'year': 1982, 'title': 'Blade Runner'}).execute(MY_CONFIG, {})
    AddDynamoItem('Movies', {'year': 1964, 'title': 'Dr. Strange Love'}).execute(MY_CONFIG, {})


@mock_dynamodb
def test_create_dynamo_item():
    from connector_aws.commands.addDynamoItem import AddDynamoItem
    create_movie_table()
    add_dynamo_item_method = AddDynamoItem('Movies', {'year': 1982, 'title': 'Blade Runner'})
    assert (add_dynamo_item_method.table_name == 'Movies')
    response = add_dynamo_item_method.execute(MY_CONFIG, {});
    assert response == {'mimetype': 'application/json', 'response': '{}'}


@mock_dynamodb
def test_query_dynamedb():
    from connector_aws.commands.queryDynamoTable import QueryDynamoTable
    create_movie_table()

    response = json.loads(QueryDynamoTable('Movies', 1982).execute(MY_CONFIG, {})['response'])
    assert response == {"Items": [], "Count": 0, "ScannedCount": 0}

    add_sample_records()
    response = json.loads(QueryDynamoTable('Movies', 1982).execute(MY_CONFIG, {})['response'])
    assert response == {'Items': [{'year': 1982, 'title': 'Blade Runner'}], 'Count': 1, 'ScannedCount': 2}


@mock_dynamodb
def test_scan_dynamodb():
    from connector_aws.commands.scanDynamoTable import ScanDynamoTable
    create_movie_table()
    add_sample_records()
    response = json.loads(ScanDynamoTable('Movies').execute(MY_CONFIG, {})['response'])
    assert response == {'Items': [
        {'year': 1982, 'title': 'Blade Runner'},
        {'year': 1964, 'title': 'Dr. Strange Love'}],
        'Count': 2, 'ScannedCount': 2}

