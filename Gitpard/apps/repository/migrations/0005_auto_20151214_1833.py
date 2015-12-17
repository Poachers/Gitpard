# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_auto_20151130_2121'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='repository',
            options={'verbose_name_plural': 'Repositories'},
        ),
    ]
