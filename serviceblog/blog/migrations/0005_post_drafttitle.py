# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20150930_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draftTitle',
            field=models.CharField(max_length=200, default=datetime.datetime(2015, 9, 30, 23, 43, 40, 361266, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
