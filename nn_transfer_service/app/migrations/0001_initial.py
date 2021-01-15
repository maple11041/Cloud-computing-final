# Generated by Django 3.0.8 on 2020-08-11 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageMakingTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(2, 'Fail'), (1, 'Success'), (3, 'Doing image now'), (0, 'Waiting')], default=0)),
                ('serial_number', models.CharField(editable=False, max_length=100, null=True, unique=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
