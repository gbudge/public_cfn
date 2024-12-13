from aws_cdk import core as cdk
from aws_cdk import aws_datasync as datasync

class datasync_stack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Source Location
        source_location = datasync.CfnLocationS3(
            self,
            "SourceLocation",
            s3_bucket_arn="arn:aws:s3:::example-source-bucket",
            subdirectory="/data",
            s3_config={
                "bucket_access_role_arn": "arn:aws:iam::123456789012:role/DataSyncAccessRole"
            },
            agent_arns=["arn:aws:datasync:region:account:agent/agent-id"]
        )

        # Destination Location
        destination_location = datasync.CfnLocationS3(
            self,
            "DestinationLocation",
            s3_bucket_arn="arn:aws:s3:::example-destination-bucket",
            subdirectory="/data",
            s3_config={
                "bucket_access_role_arn": "arn:aws:iam::123456789012:role/DataSyncAccessRole"
            },
        )

        # DataSync Task
        task = datasync.CfnTask(
            self,
            "DataSyncTask",
            source_location_arn=source_location.attr_location_arn,
            destination_location_arn=destination_location.attr_location_arn,
            options={
                "verify_mode": "POINT_IN_TIME_CONSISTENT",
                "overwrite_mode": "ALWAYS",
                "posix_permissions": "PRESERVE",
                "preserve_deleted_files": "PRESERVE",
                "preserve_devices": "NONE",
                "task_queueing": "ENABLED",
                "log_level": "TRANSFER"
            },
            schedule={
                "schedule_expression": "rate(1 day)"
            },
            tags=[{"key": "Environment", "value": "Production"}]
        )
