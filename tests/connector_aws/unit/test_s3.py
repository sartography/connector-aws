import simplejson as json
import boto3
from moto import mock_s3

MY_CONFIG = {"AWS_ACCESS_KEY_ID": "1234", "AWS_SECRET_ACCESS_KEY": "4567", "AWS_REGION": "us-east-1"}

@mock_s3
def test_my_model_save():
    from connector_aws.commands.uploadFile import UploadFileData
    conn = boto3.resource('s3', region_name='us-east-1')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    bucket_name = "my_test_bucket"
    conn.create_bucket(Bucket=bucket_name)

    # Now call the Upload File Data
    file_data = "data:application/pdf;name=Harmeet_13435%20(1).pdf;base64,JVBERi0xLjQKJZOMi54gUmVwb3J0TFiIEdlb="
    response = json.loads(UploadFileData(file_data, bucket_name, 'file.txt').execute(MY_CONFIG, {})['response'])
    assert response == {'result': 'success'}