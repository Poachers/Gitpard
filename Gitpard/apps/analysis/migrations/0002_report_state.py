# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='state',
            field=models.IntegerField(default=0, verbose_name='\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435', choices=[(-1, '\u041e\u0448\u0438\u0431\u043a\u0430 \u043f\u0440\u0438 \u0441\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d\u0438\u0438 \u043e\u0442\u0447\u0451\u0442\u0430'), (0, '\u041e\u0442\u0447\u0451\u0442 \u043f\u043e\u0434\u0433\u043e\u0442\u0430\u0432\u043b\u0438\u0432\u0430\u0435\u0442\u0441\u044f'), (1, '\u041e\u0442\u0447\u0451\u0442 \u0433\u043e\u0442\u043e\u0432')]),
            preserve_default=False,
        ),
    ]
