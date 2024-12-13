import pytest
from aws_cdk import core as cdk
from aws_cdk.assertions import Template
from datasync_stack import datasync_stack  # Assuming this is the class name and file name

@pytest.fixture
def app():
    return cdk.App()

@pytest.fixture
def stack(app):
    return test_datasync_stack(app, "TestStack")

def test_stack_resources(stack):
    # Generate the CloudFormation template
    template = Template.from_stack(stack)

    # Check for the existence of source S3 location
    template.has_resource_properties("AWS::DataSync::LocationS3", {
        "S3BucketArn": "arn:aws:s3:::example-source-bucket",
        "Subdirectory": "/data",
        "S3Config": {
            "BucketAccessRoleArn": "arn:aws:iam::123456789012:role/DataSyncAccessRole"
        },
        "AgentArns": ["arn:aws:datasync:region:account:agent/agent-id"]
    })

    # Check for the existence of destination S3 location
    template.has_resource_properties("AWS::DataSync::LocationS3", {
        "S3BucketArn": "arn:aws:s3:::example-destination-bucket",
        "Subdirectory": "/data",
        "S3Config": {
            "BucketAccessRoleArn": "arn:aws:iam::123456789012:role/DataSyncAccessRole"
        }
    })

    # Check for the existence of the DataSync task
    template.has_resource_properties("AWS::DataSync::Task", {
        "SourceLocationArn": {
            "Ref": "SourceLocation"
        },
        "DestinationLocationArn": {
            "Ref": "DestinationLocation"
        },
        "Options": {
            "VerifyMode": "POINT_IN_TIME_CONSISTENT",
            "OverwriteMode": "ALWAYS",
            "PosixPermissions": "PRESERVE",
            "PreserveDeletedFiles": "PRESERVE",
            "PreserveDevices": "NONE",
            "TaskQueueing": "ENABLED",
            "LogLevel": "TRANSFER"
        },
        "Schedule": {
            "ScheduleExpression": "rate(1 day)"
        },
        "Tags": [
            {"Key": "Environment", "Value": "Production"}
        ]
    })
