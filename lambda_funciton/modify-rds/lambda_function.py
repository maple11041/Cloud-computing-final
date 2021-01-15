import sys
import pymysql
from urllib.parse import unquote_plus

#rds settings
rds_host  = "database-3.c9mxeruaextg.us-east-1.rds.amazonaws.com"
name ="Yanting"
password = "Yanting1234"
db_name = "record" 


conn = pymysql.connect(host= rds_host, user=name, passwd=password, db=db_name)


def lambda_handler(event, context):
    """
    This function fetches content from MySQL RDS instance
    """
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        
        print( f"{bucket} : {key}")
        item_count = 0
    
        with conn.cursor() as cur:
            sql= "UPDATE `app_transferrecord` SET `new_bucket`=%s WHERE `new_key`=%s;"
            cur.execute(sql,('pre-image-after-texture',key,))
            sql= "UPDATE `app_transferrecord` SET `status`=1 WHERE `new_key`=%s;"
            cur.execute(sql,(key,))
            # cur.execute("select * from Employee")
        conn.commit()

    


mock_data = {
  "Records": [
    {
      "eventVersion": "2.0",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "1970-01-01T00:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "EXAMPLE"
      },
      "requestParameters": {
        "sourceIPAddress": "127.0.0.1"
      },
      "responseElements": {
        "x-amz-request-id": "EXAMPLE123456789",
        "x-amz-id-2": "EXAMPLE123/5678abcdefghijklambdaisawesome/mnopqrstuvwxyzABCDEFGH"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "testConfigRule",
        "bucket": {
          "name": "pre-image",
          "ownerIdentity": {
            "principalId": "EXAMPLE"
          },
          "arn": "arn:aws:s3:::pre-image"
        },
        "object": {
          "key": "wave__d60f0c2b-4d0e-42a3-b54c-7e98e4ad81ae.png",
          "size": 1024,
          "eTag": "0123456789abcdef0123456789abcdef",
          "sequencer": "0A1B2C3D4E5F678901"
        }
      }
    }
  ]
}
lambda_handler(mock_data,'')