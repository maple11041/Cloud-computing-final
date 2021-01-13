import boto3
import os
import sys
import uuid
import mysql.connector
from datetime import datetime
import requests
import time


# import PIL.Image


def upload_aws_lambda(path, bucket="pre-image"):
    s3_client = boto3.client('s3')
    # bucket = 'pre-image'
    key = path.split('/')[-1]
    print(key)
    # downlaod_path = './test1.jpg'
    # s3_client.download_file(bucket, key, downlaod_path)
    upload_path = path
    s3_client.upload_file(upload_path, bucket, key)


def download_aws_lambda(path, new_key, new_bucket):
    s3_client = boto3.client('s3')
    print(path, new_key, new_bucket)
    # bucket = 'pre-image-resized'
    # key = path.split('/')[-1]
    # print(key)
    # downlaod_path = './test1.jpg'
    # s3_client.download_file(bucket, key, downlaod_path)
    download_path = path
    print(download_path)
    # s3_client.upload_file(upload_path, bucket, key)
    s3_client.download_file(new_bucket, new_key, download_path)
    return True


def upload_dl_transfer(path, style):
    bucket = "pre-image"
    upload_aws_lambda(path=path)
    old_key = path.split('/')[-1]
    mydb = mysql.connector.connect(host="database-3.c9mxeruaextg.us-east-1.rds.amazonaws.com",
                                   user="Yanting", password="Yanting1234", database="record")

    mycursor = mydb.cursor()
    print(mydb.is_connected())
    # now = datetime.now()
    sql = "INSERT INTO app_transferrecord(transfer_style, org_bucket, old_key) VALUES (%s, %s ,%s )"
    val = (int(style), bucket, old_key)
    # sql = "SELECT * FROM app_transferrecord WHERE status = 0"
    mycursor.execute(sql, val)

    mydb.commit()
    print(mycursor.rowcount)
    r = requests.get("http://140.112.42.22:8124/Image")
    print(r)
    sql_search = "SELECT status, new_key, new_bucket FROM app_transferrecord WHERE old_key = %s"
    query_key = (old_key, )
    new_key = None
    new_bucket = None
    for i in range(70):
        time.sleep(1)
        mycursor.execute(sql_search, query_key)
        myresult = mycursor.fetchall()
        mydb.commit()
        print(myresult[0][0], myresult[0][1], myresult[0][2])
        if (myresult[0][0] == 1):
            new_key = myresult[0][1]
            new_bucket = myresult[0][2]
            break
    save_path = os.path.join("transfered", new_key)
    download_aws_lambda(save_path, new_key, new_bucket)
    return save_path
    # print(myresult)


# upload_dl_transfer(path="./image/test123.jpg")
# WAITING = 0
#     FAIL = 2
#     SUCCESS = 1
#     STATUS = [
#         (FAIL, 'Fail'),
#         (SUCCESS, 'Success'),
#         (WAITING, 'Waiting'),
#     ]

#     style_list = [(0,'wave'),
#             (1,'la_muse'),(2,'rain_princess'),(3,'the_scream'),
#             (4,'udnie'),(5,'the_shipwreck_of_the_minotaur')
#     ]
# status = models.SmallIntegerField(choices=STATUS, default=WAITING)
# transfer_style = models.SmallIntegerField(choices=style_list, default=0) # int required
# org_bucket = models.CharField(max_length=100, null=True, editable=False,default='pre-image') # required
# new_bucket = models.CharField(max_length=100, null=True, editable=False,default='pre-image-after')
# key = models.CharField(max_length=100, unique=False, null=True, editable=False) # required
# new_key = models.CharField(max_length=100, unique=True, null=True, editable=False)
# create_at = models.DateTimeField(auto_now_add=True)
# update_at = models.DateTimeField(auto_now=True)
