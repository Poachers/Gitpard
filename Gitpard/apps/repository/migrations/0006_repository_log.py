# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_auto_20151214_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='log',
            field=models.TextField(verbose_name='\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0435', blank=True),
        ),
    ]
