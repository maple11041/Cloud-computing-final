# Generated by Django 2.2 on 2021-01-13 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20210112_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferrecord',
            name='org_bucket',
            field=models.CharField(default='pre-image-after', editable=False, max_length=100, null=True),
        ),
    ]