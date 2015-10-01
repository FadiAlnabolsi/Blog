# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import blog.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_asset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset',
            field=models.FileField(upload_to=blog.models.slugified_file_location, max_length=50),
        ),
    ]
