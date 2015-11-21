# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0004_auto_20151121_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='path',
            field=models.CharField(max_length=140, verbose_name='\u041f\u0443\u0442\u044c \u0434\u043e \u043e\u0442\u0447\u0451\u0442\u0430 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0435', blank=True),
        ),
    ]
