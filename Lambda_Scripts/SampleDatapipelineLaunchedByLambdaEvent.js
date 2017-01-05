{
  "objects": [
    {
      "taskInstanceType": "#{myTaskInstanceType}",
      "bootstrapAction": "#{myBootstrapAction}",
      "taskInstanceCount": "#{myTaskInstanceCount}",
      "name": "EmrClusterObj",
      "coreInstanceType": "#{myCoreInstanceType}",
      "keyPair": "#{myEC2KeyPair}",
      "coreInstanceCount": "#{myCoreInstanceCount}",
      "masterInstanceType": "#{myMasterInstanceType}",
      "amiVersion": "#{myEMRAMIVersion}",
      "id": "EmrClusterObj",
      "type": "EmrCluster",
      "terminateAfter": "50 Minutes"
    },
    {
      "occurrences": "1",
      "period": "1 Day",
      "name": "RunOnce",
      "id": "DefaultSchedule",
      "type": "Schedule",
      "startAt": "FIRST_ACTIVATION_DATE_TIME"
    },
    {
      "failureAndRerunMode": "CASCADE",
      "schedule": {
        "ref": "DefaultSchedule"
      },
      "resourceRole": "DataPipelineDefaultResourceRole",
      "role": "DataPipelineDefaultRole",
      "pipelineLogUri": "s3://aws-logs-046845663771-us-east-1/",
      "scheduleType": "cron",
      "name": "Default",
      "id": "Default"
    },
    {
      "role": "DataPipelineDefaultRole",
      "subject": "EMR analysis Failure",
      "name": "DefaultAction2",
      "id": "ActionId_NaccK",
      "type": "SnsAlarm",
      "message": "EMR analysis Failure",
      "topicArn": "arn:aws:sns:us-east-1:046845663771:ClientPUT"
    },
    {
      "onFail": {
        "ref": "ActionId_NaccK"
      },
      "name": "EmrActivityObj",
      "step": "#{myEmrStep}",
      "runsOn": {
        "ref": "EmrClusterObj"
      },
      "id": "EmrActivityObj",
      "type": "EmrActivity"
    },
    {
      "role": "DataPipelineDefaultRole",
      "subject": "EMR analysis successful",
      "name": "DefaultAction1",
      "id": "ActionId_yLe3G",
      "message": "EMR analysis successful",
      "type": "SnsAlarm",
      "topicArn": "arn:aws:sns:us-east-1:046845663771:ClientPUT"
    }
  ],
  "parameters": [
    {
      "helpText": "An existing EC2 key pair to SSH into the master node of the EMR cluster as the user \"hadoop\".",
      "description": "EC2 key pair",
      "optional": "true",
      "id": "myEC2KeyPair",
      "type": "String"
    },
    {
      "helpLink": "https://docs.aws.amazon.com/console/datapipeline/emrsteps",
      "watermark": "s3://myBucket/myPath/myStep.jar,firstArg,secondArg",
      "helpText": "A step is a unit of work you submit to the cluster. You can specify one or more steps",
      "description": "EMR step(s)",
      "isArray": "true",
      "id": "myEmrStep",
      "type": "String"
    },
    {
      "helpText": "Task instances run Hadoop tasks.",
      "description": "Task node instance type",
      "optional": "true",
      "id": "myTaskInstanceType",
      "type": "String"
    },
    {
      "default": "m1.medium",
      "helpText": "Core instances run Hadoop tasks and store data using the Hadoop Distributed File System (HDFS).",
      "description": "Core node instance type",
      "id": "myCoreInstanceType",
      "type": "String"
    },
    {
      "default": "2.4.8",
      "helpText": "Determines the base configuration of the instances in your cluster, including the Hadoop version.",
      "description": "EMR AMI version",
      "id": "myEMRAMIVersion",
      "type": "String"
    },
    {
      "default": "2",
      "description": "Core node instance count",
      "id": "myCoreInstanceCount",
      "type": "Integer"
    },
    {
      "description": "Task node instance count",
      "optional": "true",
      "id": "myTaskInstanceCount",
      "type": "Integer"
    },
    {
      "helpLink": "https://docs.aws.amazon.com/console/datapipeline/emr_bootstrap_actions",
      "helpText": "Bootstrap actions are scripts that are executed during setup before Hadoop starts on every cluster node.",
      "description": "Bootstrap action(s)",
      "isArray": "true",
      "optional": "true",
      "id": "myBootstrapAction",
      "type": "String"
    },
    {
      "default": "m1.medium",
      "helpText": "The Master instance assigns Hadoop tasks to core and task nodes, and monitors their status.",
      "description": "Master node instance type",
      "id": "myMasterInstanceType",
      "type": "String"
    }
  ],
  "values": {
    "myMasterInstanceType": "m1.medium",
    "myBootstrapAction": "s3://configsbucket/mybootstrap.sh",
    "myEMRAMIVersion": "3.8.0",
    "myEC2KeyPair": "myAdminEast",
    "myEmrStep": "s3://elasticmapreduce/libs/script-runner/script-runner.jar,s3://configsbucket/mystreaming.sh",
    "myCoreInstanceCount": "2",
    "myCoreInstanceType": "m1.medium"
  }
}