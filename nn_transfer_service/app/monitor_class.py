from threading import Lock, Thread
from .os_control import rm_file, gen_file_pathes, cp_file
from .models import TransferRecord
import os
import time
import requests
import queue
import inspect
import ctypes
from django.db import connection, transaction
import logging
from django.conf import settings
import json
import subprocess
from pathlib import Path
import boto3
import functools
import os

import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image


logger = logging.getLogger(__name__)

instance = None
insert_queue = queue.Queue()
instance_lock = Lock()
new_bucket = 'pre-image-after'

def return_instance():
    global instance
    return instance


def add_task(bucket='', key=''):
    global instance, insert_queue
    if bucket!='' and key!='':
        download_s3_file(bucket,key)
    
    if not isinstance(instance, Monitor_Service) or not instance.isAlive():
        with instance_lock:
            logger.debug('make new thread')
            time.sleep(2)
            instance = Monitor_Service(insert_queue)
        instance.start()

    else:
        logger.debug(f'already a thread!!!')


def restart(insert_queue):
    global instance
    with instance_lock:
        instance = None
        # instance = Thread(target=Monitor_Service,
        #                   args=insert_queue,
        #                   daemon=False)
        # instance.start()

def download_s3_file(bucket,key):
    download_path = os.path.join('./img_dir/',key)
    s3_client = boto3.client('s3')
    print(bucket,key)
    s3_client.download_file(bucket, key, download_path)
    logger.debug(f'download_file {key} image')

class Monitor_Service(Thread):

    def __init__(self, insert_queue):
        Thread.__init__(self)
        # StoppableThread.__init__(self)
        RM_ip = settings.RM_IP
        self.insert_queue = insert_queue
        self.style_list  = ['wave.jpg','la_muse.jpg','rain_princess.jpg','the_scream.jpg',"udnie.jpg","the_shipwreck_of_the_minotaur.jpg"]
        self.style_dir = "./style/"
        
       
        logger.debug('initializing start')

    def run(self):
        self.monitoring()
        """
        try:
            self.monitoring()
        except Exception as e :
            logger.debug('Exception happen!!')
            logger.error(e)
            restart(self.insert_queue)
        """
        

    def crop_center(self,image):
        """Returns a cropped square image."""
        shape = image.shape
        new_shape = min(shape[1], shape[2])
        offset_y = max(shape[1] - shape[2], 0) // 2
        offset_x = max(shape[2] - shape[1], 0) // 2
        image = tf.image.crop_to_bounding_box(
            image, offset_y, offset_x, new_shape, new_shape)
        return image


    def load_image(self,image_path, image_size=(256, 256), preserve_aspect_ratio=True):
        """Loads and preprocesses images."""
        # Cache image file locally.
        # image_path = tf.keras.utils.get_file(os.path.basename(image_url)[-128:], image_url)
        # Load and convert to float32 numpy array, add batch dimension, and normalize to range [0, 1].
        img = plt.imread(image_path).astype(np.float32)[np.newaxis, ...,:3]
        if img.max() > 1.0:
            img = img / 255.
        if len(img.shape) == 3:
            img = tf.stack([img, img, img], axis=-1)
        img = self.crop_center(img)
        img = tf.image.resize(img, image_size, preserve_aspect_ratio=True)
        return img


    def monitoring(self):
        logger.debug('start monitor')
        hub_module = hub.load('nn_transfer.h5')
        while True:

            if TransferRecord.objects.filter(status=0).count() == 0:
                break
            
            # whole_list = TransferRecord.objects.order_by('create_at')
            # for each_task in TransferRecord.objects.filter(status=0):
            each_task = TransferRecord.objects.filter(status=0).order_by('pk')[0]
            key = each_task.old_key 
            download_path = os.path.join('./img_dir/',key)
            if not os.path.exists(download_path):
                download_s3_file(each_task.org_bucket,key)
            style_path = os.path.join(self.style_dir,self.style_list[ each_task.transfer_style])
            output_image_size = 384 
            content_img_size = (output_image_size, output_image_size)

            style_img_size = (256, 256)  # Recommended to keep it at 256.

            content_image = self.load_image(download_path)
            
            style_image = self.load_image(style_path, style_img_size)
            style_image = tf.nn.avg_pool(style_image, ksize=[3,3], strides=[1,1], padding='SAME')
            
            outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
            stylized_image = outputs[0]
            new_key = self.style_list[ each_task.transfer_style].split('.')[0]+'__'+key
            upload_path =f"./tmp_results/{new_key}"
            tf.keras.preprocessing.image.save_img(upload_path, stylized_image[0])
            s3_client = boto3.client('s3')
            s3_client.upload_file(upload_path,new_bucket, new_key )
            each_task.status = 3
            each_task.new_bucket = new_bucket
            each_task.new_key = new_key.replace('.jpg','.png')
            each_task.save()
            print('complete : ',new_key)


                
        logger.debug('monitor end')
        connection.close()

    

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        logger.debug("thread already gone")
        pass
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread():
    global instance
    _async_raise(instance.ident, SystemExit)
    instance = None
    connection.close()
    logger.debug('======thread force stop=====')
