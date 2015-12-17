# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20151121_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='state',
            field=models.IntegerField(default=0, verbose_name='\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u044f.', choices=[(0, '\u041d\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d'), (1, '\u0417\u0430\u0433\u0440\u0443\u0436\u0430\u0435\u0442\u0441\u044f'), (2, '\u0417\u0430\u0433\u0440\u0443\u0436\u0435\u043d'), (3, '\u041e\u0431\u043d\u043e\u0432\u043b\u044f\u0435\u0442\u0441\u044f'), (-1, '\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c'), (-2, '\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u043e\u0431\u043d\u043e\u0432\u0438\u0442\u044c'), (4, '\u0414\u043e\u0441\u0442\u0443\u043f \u0437\u0430\u0431\u043b\u043e\u043a\u0438\u0440\u043e\u0432\u0430\u043d')]),
        ),
    ]
