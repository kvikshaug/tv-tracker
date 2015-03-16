# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150316_1913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='season',
            old_name='show',
            new_name='series',
        ),
    ]
