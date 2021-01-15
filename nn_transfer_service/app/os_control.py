import os, time, glob
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, as_completed
from .models import ImageMakingTask
import logging
from django.conf import settings


logger = logging.getLogger(__name__)
#result2 = os.path.exists(file_path)
# list dir : 'dir Z:\\' 
# fail to use 'cd \\taicmitdiv02.auth.hpicorp.net\PO_IN due to powershell' not support
PRISM_SERVER = settings.PRISM_SERVER  # "\\\\taicmitdiv02.auth.hpicorp.net"
FITB_dir = settings.FITB_WORK_DIR  #'C:\\Users\\WengYanT\\Documents\\http_ser\\fake_fitb_dir'
# FITB_dir = 'c:\\VCOSMOSFITB\\Job'


class fileRemoveError(Exception):
    pass


class fileMissError(Exception):
    pass


class fileCopyError(Exception):
    pass


class GenPofileTimeout(Exception):
    pass


class GenImageError(Exception):
    pass


class fileRenameError(Exception):
    pass


def clean_dir():
    path = FITB_dir+'\\*'
    files = glob.glob(path)
    for f in files:
        os.remove(f)


def rm_file(file):
    if os.path.exists(file):
        if os.system(f"del {file}"):
            logger.warning(f'can not remove {file}.')
            raise fileRemoveError
    # logger.debug(f"remove {file} complete.")
    return
    # os.system("copy C:\\Users\\WengYanT\\Documents\\ZBook_15u_G6_Mobile_W.IN \\\\taicmitdiv02.auth.hpicorp.net\\PO_IN")


def cp_file(src_file, dst_file):
    if not os.path.exists(src_file):
        logger.warning(f'can not find {src_file} when copy.')
        raise fileMissError
    if os.system(f"copy {src_file} {dst_file}"):
        logger.warning(f'copy from {src_file} to  {dst_file} fail .')
        raise fileCopyError
    else:
        logger.debug(f'copy complete')
        return True

def ren_file(src_file, dst_file):
    if not os.path.exists(src_file):
        logger.warning(f'can not find {src_file} when copy.')
        raise fileMissError
    logger.warning(f'rename from {src_file} to  {dst_file}.')
    if os.system(f"move {src_file} {dst_file}"):
        logger.warning(f'rename from {src_file} to  {dst_file} fail .')
        raise fileRenameError
    else:
        logger.debug(f'rename  {src_file} {dst_file} complete')
        return True

def wait_until(condtion_func, interval, count, timeout_raise):
    _count = 0
    while condtion_func() is False:
        time.sleep(interval)
        _count += 1
        if _count > count:
            raise timeout_raise


def gen_file_pathes(serial_number):
    po_out_dir_name = 'PoFiles'
    po_in_dir_name = 'PO_IN'
    path_dict = {
                'fitb_done_file_name': os.path.join(FITB_dir, f'{serial_number}.don'),
                'fitb_fail_file_name': os.path.join(FITB_dir, f'{serial_number}.err'),
                'fitb_job_file_name': os.path.join(FITB_dir, f'{serial_number}.job'),
                'fitb_pro_file_name': os.path.join(FITB_dir, f'{serial_number}.pro'),
                'fitb_finalpro_file_name': os.path.join(FITB_dir, f'{serial_number}.finalpro'),
                'fitb_warn_file_name': os.path.join(FITB_dir, f'{serial_number}.warn'),
                'po_out_file_path': os.path.join(PRISM_SERVER, po_out_dir_name, serial_number),
                'fail_po_out_file_path': os.path.join(PRISM_SERVER, po_out_dir_name, f'{serial_number}.ERR'),
                'po_in_file_path': os.path.join(PRISM_SERVER, po_in_dir_name, f'{serial_number}.IN')
                
                }
    return path_dict


def edit_po(src_path, partno, content):
    with open(src_path, 'ab+') as f:
        windows_new_line = '\r\n'
        f.write(bytes(f'{windows_new_line}'.join(partno), encoding='utf-8'))
        f.write(bytes(f'{windows_new_line}', encoding='utf-8'))
        f.write(bytes(content, encoding='utf-8'))
        f.seek(0)


def main_task(st):
    SOURCE_file = os.path.dirname(__file__)

    serial_number = st*10
    path_dict = gen_file_pathes(serial_number)
    # temp file store
    poin_src_path = os.path.join(SOURCE_file, 'PO_IN_file', f'{serial_number}.IN')
    # remove privious POout
    rm_file(path_dict['po_out_file_path'])
    rm_file(path_dict['fail_po_out_file_path'])
    # put POin in PRISM
    logger.debug(f'po in {poin_src_path}')
    cp_file(poin_src_path, path_dict['po_in_file_path'])
    # wait POout in generate
    wait_until(lambda: os.path.exists(path_dict['po_out_file_path'])
                    or os.path.exists(path_dict['fail_po_out_file_path']),
                    interval=0.5, count=120, timeout_raise=GenPofileError)

    if os.path.exists(path_dict['po_out_file_path']):
        logger.debug('PO out generate!')
    else:
        raise GenPofileError
    # put POout to FITB work dir
    rm_file(path_dict['fitb_done_file_name'])
    rm_file(path_dict['fitb_fail_file_name'])
    cp_file(path_dict['po_out_file_path'], path_dict['fitb_job_file_name'])
    wait_until(lambda: os.path.exists(path_dict['fitb_done_file_name'])
                or os.path.exists(path_dict['fitb_fail_file_name']),
                interval=5, count=60, timeout_raise=GenPofileError)
    if os.path.exists(path_dict['fitb_done_file_name']):
        logger.debug('Image generate complete!')
    else :
        raise GenImageError
    return True


def main(*args):
    fn = main_task
    test_list = ['A', 'T', 'C', 'X']
    worker_count = None
    if isinstance(worker_count, int):
        pool = ThreadPoolExecutor(max_workers=worker_count)
    else:
        pool = ThreadPoolExecutor()
    logger.debug(f'test for {fn.__name__}')

    with pool:
        futures = [pool.submit(fn, st) for st in test_list]
        # [future.result() for future in as_completed(futures)]
        results = [future.result() for future in as_completed(futures)]
    for result in results:
        logger.debug(result)
    '''
    try:
        assert all((result is True for result in results))
    except AssertionError:
        logger.debug(f'{fn.__name__} fail')
    else:
        logger.debug(f'{fn.__name__} is good')
    '''    

if __name__ == "__main__":
    main()
