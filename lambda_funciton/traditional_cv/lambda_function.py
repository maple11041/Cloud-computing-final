import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image, ImageDraw, ImageFont
import PIL.Image

s3_client = boto3.client('s3')


def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        print(image.size)
        # image.thumbnail(tuple(x / 2 for x in image.size))
        image = image.resize((256,256),Image.ANTIALIAS)
        print(image.size)
        image.save(resized_path)


def to_mosaic(file_name):
    width = 256
    height = 256
    granularity = 10  # 颗粒度
    image_file = Image.open(file_name)
    image_file = image_file.convert('RGB')
    print(image_file.size)
    image = Image.new('RGB', (width, height), (255, 255, 255))

    # 创建Draw对象:
    draw = ImageDraw.Draw(image)
    for x in range(0, width, granularity):
        for y in range(0, height, granularity):
            r, g, b = image_file.getpixel((x, y))
            draw.rectangle([(x, y), (x + granularity, y + granularity)], fill=(r, g, b), outline=None)  # None即是不加网格
    final_file_name = file_name.replace(".jpg",'.png')
    image.save(final_file_name)
    return final_file_name


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/resized-{}'.format(tmpkey)
        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        upload_path = to_mosaic(upload_path)
        i.upload_file(upload_path, '{}-resized'.format(bucket), key.replace(".jpg",'.png'))
        
        


# key = '../sample_img/content/chicago.jpg'
# tmpkey = key.replace('/', '')
# download_path = key
# upload_path = './tmp/resized-{}'.format(tmpkey)
# resize_image(download_path, upload_path)
# to_mosaic(upload_path)
