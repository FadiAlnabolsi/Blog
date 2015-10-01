# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import blog.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('asset', models.FileField(help_text='\n            <strong>Document: </strong>pdf, docx, odt, rtf, txt, xlsx, csv, zip<br />\n            <strong>Image: </strong>png, jpg, jpeg, bmp, gif<br />\n        ', max_length=50, upload_to=blog.models.slugified_file_location)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
    ]
