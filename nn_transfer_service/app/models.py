from django.db import models


class ImageMakingTask(models.Model):
    WAITING = 0
    FAIL = 2
    SUCCESS = 1
    DOING = 3
    STATUS = [
        (FAIL, 'Fail'),
        (SUCCESS, 'Success'),
        (DOING, 'Doing image now'),
        (WAITING, 'Waiting'),
    ]
    status = models.SmallIntegerField(choices=STATUS, default=WAITING)
    serial_number = models.CharField(max_length=100, unique=True,
                                     null=True, editable=False)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Serial number: {self.serial_number},Status:{self.status}'


class TransferRecord(models.Model):
    WAITING = 0
    FAIL = 2
    SUCCESS = 1
    DONING = 3
    STATUS = [
        (FAIL, 'Fail'),
        (SUCCESS, 'Success'),
        (WAITING, 'Waiting'),
        (DONING, 'Doing'),
    ]
    
    style_list = [(0,'wave'),
            (1,'la_muse'),(2,'rain_princess'),(3,'the_scream'),
            (4,'udnie'),(5,'the_shipwreck_of_the_minotaur')
    ]
    status = models.SmallIntegerField(choices=STATUS, default=WAITING)
    transfer_style = models.SmallIntegerField(choices=style_list, default=0)
    org_bucket = models.CharField(max_length=100,
                                null=True, editable=False,default='pre-image')
    new_bucket = models.CharField(max_length=100,
                                null=True, editable=False,default='pre-image-after')
    old_key = models.CharField(max_length=100, unique=False,
                                     null=True, editable=False)
    new_key = models.CharField(max_length=100, unique=True,
                                     null=True, editable=False)

    def __str__(self):
        return f'old key: {self.old_key},status:{self.status}'

