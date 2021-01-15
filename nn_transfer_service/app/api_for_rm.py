from threading import Thread
from django.views.generic.base import View
from django.http import HttpResponse
import json
import os
from .os_control import rm_file, gen_file_pathes, wait_until, cp_file,\
                        fileRemoveError, GenPofileTimeout, fileMissError,\
                        fileCopyError,\
                        edit_po
from .monitor_class import add_task
import logging
import subprocess
from django.conf import settings
from pathlib import Path
from string import Template
logger = logging.getLogger(__name__)
from urllib.parse import unquote_plus
import boto3


# class PoinAPI(View):   
#     http_method_names = ['post', 'get']
    
#     def post(self, request):
#         raw_info = json.loads(request.body)
#         try:
#             if self.post_POin(raw_info):
#                 logger.debug(f'POfile: { raw_info["serial_number"] } generated')
#                 return HttpResponse(status=204)  # not sure
#             else:
#                 logger.warning(f'{ raw_info["serial_number"] }.err file generated due to wrong PoinFile!!!')
#                 return HttpResponse(status=422)
#         except fileRemoveError:
#             logger.error('file remove error')
#             return HttpResponse(status=500)
#         except GenPofileTimeout:
#             logger.error('Pofile generate timeout')
#             return HttpResponse(status=500)
#         except Exception as e:
#             logger.error(e)
#             return HttpResponse(status=500)

#     def get(self, request):
#         return HttpResponse("Dash page.")

#     def post_POin(self, raw_info):
#         path_dict = gen_file_pathes(raw_info['serial_number'])
#         rm_file(path_dict['po_out_file_path'])
#         rm_file(path_dict['fail_po_out_file_path'])
#         rm_file(path_dict['po_in_file_path'])

#         with open(pintervalath_dict['po_in_file_path'], 'wb+') as f:
#             f.write(bytes(raw_info['POFile'], encoding='utf-8'))
#             f.seek(0)

#         wait_until(lambda: os.path.exists(path_dict['po_out_file_path'])
#                    or os.path.exists(path_dict['fail_po_out_file_path']),
#                    =0.5, count=120, timeout_raise=GenPofileTimeout)

#         if os.path.exists(path_dict['po_out_file_path']):
#             return True
#         else:
#             return False
#         # return HttpResponse("Dash page.")


class ImageAPI(View):
    http_method_names = ['post', 'get']

    def post(self, request):
        raw_info = json.loads(request.body)
        
        for record in raw_info['Records']:
            bucket = record['s3']['bucket']['name']
            key = unquote_plus(record['s3']['object']['key'])
            #download_path = os.path.join('./img_dir/',key)
            print(key)
            #self.gen_image_start(bucket, key, download_path)
            #add_task()
            #"""
            try:
                #self.gen_image_start(bucket, key, download_path)
                add_task(bucket, key)
            except Exception as e:
                logger.error(e)
                return HttpResponse(status=500)
            #"""
            
            return HttpResponse(status=204)
            

    def get(self, request):
        try:
            #add_task(bucket, key)
            add_task()
        except Exception as e:
            logger.error(e)
            return HttpResponse(status=500)
        return HttpResponse(status=204)
        #return HttpResponse("Image page.")

    
    # def create_content(self, raw_info):
    #     rm_ip = raw_info['rm_ip']
    #     rm_port = raw_info['rm_port']
    #     server_location = raw_info['prism_sserver']
    #     blobsserver = raw_info['prism_blobsserver']

    #     header_template = Template('*' * 10 + ' ' * 2 + '$header' + ' ' * 2 + '*' * 10)
    #     header_for_PieAutoDash = header_template.substitute(header='vCosmos Information')
    #     information = {'RM_IP': rm_ip, 'RM_PORT': rm_port}
    #     information_content = [f'{key}={value}' for key, value in information.items()]

    #     header_for_vCosmos = header_template.substitute(header='vCosmos Config')    
    #     config = {'rm': {'ip': rm_ip, 'port': rm_port},
    #               'prism': {'sserver': server_location, 'blobsserver': blobsserver},
    #               }

    #     _config_content = json.dumps(config, separators=(',', ':'))
    #     config_content = f'vCosmos-config:{_config_content}:config-end'

    #     lines = [
    #         header_for_PieAutoDash,
    #         *information_content,
    #         '',
    #         header_for_vCosmos,
    #         config_content
    #     ]

    #     po_file_comment_mark = ';'
    #     content = '\n'.join(
    #         map(lambda line: f'{po_file_comment_mark}{line}', lines))
    #     return content
