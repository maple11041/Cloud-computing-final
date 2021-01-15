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


def texture(file_name):
    imageA=Image.open(file_name)
    imageB=Image.open('./transfer-removebg-preview.png')
    imageA = imageA.convert('RGBA')
    imageB = imageB.convert('RGBA')
    widthA , heightA = imageA.size
    widthB , heightB = imageB.size
    newWidthB = int(widthA/2)
    newHeightB = int(heightB/widthB*newWidthB)
    imageB_resize = imageB.resize((newWidthB, newHeightB))
    resultPicture = Image.new('RGBA', imageA.size, (0, 0, 0, 0))
    resultPicture.paste(imageA,(0,0))
    right_bottom = (widthA - newWidthB, heightA - newHeightB)
    resultPicture.paste(imageB_resize, right_bottom, imageB_resize)

    final_file_name = file_name.replace(".jpg",'.png')
    resultPicture.save(final_file_name)
    return final_file_name


def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/texture-{}'.format(tmpkey)
        s3_client.download_file(bucket, key, download_path)
        # resize_image(download_path, upload_path)
        #final_file_name = texture(upload_path)
        final_file_name = texture(download_path)
        s3_client.upload_file(final_file_name, '{}-texture'.format(bucket), key.replace(".jpg",'.png'))
        


# key = '../sample_img/content/chicago.jpg'
# tmpkey = key.replace('/', '')
# download_path = key
# upload_path = './tmp/resized-{}'.format(tmpkey)
# resize_image(download_path, upload_path)
# texture(upload_path)
