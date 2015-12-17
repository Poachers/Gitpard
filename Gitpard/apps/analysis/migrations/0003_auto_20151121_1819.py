# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_report_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='mask',
            field=models.TextField(verbose_name='\u041c\u0430\u0441\u043a\u0430'),
        ),
        migrations.AlterField(
            model_name='report',
            name='report',
            field=models.TextField(verbose_name='\u041e\u0442\u0447\u0451\u0442', blank=True),
        ),
    ]
