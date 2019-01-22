import boto3
import os
import json
import decimal

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

class DynamoDB:
    def __init__(self, endpoint_url=None):
        self.session = boto3.session.Session(
            aws_access_key_id = os.environ['AWS_ACCESS_KEY'],
            aws_secret_access_key = os.environ['AWS_SECRET_KEY'],
            region_name = os.environ['AWS_REGION']
        )

        self.client = self.session.client('dynamodb', endpoint_url=endpoint_url) if endpoint_url else self.session.client('dynamodb')
        self.resource = self.session.resource('dynamodb', endpoint_url=endpoint_url) if endpoint_url else self.session.resource('dynamodb')

    def get_pre_req_table(self):
        try:
            return self.client.create_table(
                TableName='pre_req',
                KeySchema=[
                    {
                        'AttributeName': 'course_key',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'course_key',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 10,
                    'WriteCapacityUnits': 10
                }
            )
        except self.client.exceptions.ResourceInUseException:
            return self.resource.Table('pre_req')

    def get_post_req_table(self):
        try:
            return self.client.create_table(

            )
        except self.client.exceptions.ResourceInUseException:
            return self.resource.Table('post_req')

    def get_all_entries(self, table):
        # return [json.dumps(i, cls=DecimalEncoder) for i in table.scan()['Items']]
        return [i for i in table.scan()['Items']]