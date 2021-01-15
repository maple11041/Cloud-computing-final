import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image, ImageDraw, ImageFont
import PIL.Image
import PIL.ImageOps 

s3_client = boto3.client('s3')


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        print(image.size)
        # image.thumbnail(tuple(x / 2 for x in image.size))
        image = image.resize((256,256),Image.ANTIALIAS)
        print(image.size)
        image.save(resized_path)


def inverse(file_name):
    image=Image.open(file_name)
    image=image.convert('RGBA')
    r,g,b,a = image.split()
    rgb_image = Image.merge('RGB', (r,g,b))

    inverted_image = PIL.ImageOps.invert(rgb_image)

    r2,g2,b2 = inverted_image.split()

    final_transparent_image = Image.merge('RGBA', (r2,g2,b2,a))
    final_file_name = file_name.replace(".jpg",'.png')
    final_transparent_image.save(file_name.replace(".jpg",'.png'))
    return final_file_name
    


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/inverse-{}'.format(tmpkey)
        s3_client.download_file(bucket, key, download_path)
        # resize_image(download_path, upload_path)
        #final_file_name = inverse(upload_path)
        final_file_name = inverse(download_path)
        s3_client.upload_file(final_file_name, '{}-texture'.format(bucket), key.replace(".jpg",'.png'))
        


# key = '../sample_img/content/chicago.jpg'
# tmpkey = key.replace('/', '')
# download_path = key
# upload_path = './tmp/resized-{}'.format(tmpkey)
# resize_image(download_path, upload_path)
# to_mosaic(upload_path)
