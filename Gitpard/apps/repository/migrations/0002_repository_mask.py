# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='mask',
            field=models.CharField(max_length=1000, verbose_name='\u041c\u0430\u0441\u043a\u0430', blank=True),
        ),
    ]
