# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_repository_mask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='mask',
            field=models.TextField(verbose_name='\u041c\u0430\u0441\u043a\u0430', blank=True),
        ),
    ]
