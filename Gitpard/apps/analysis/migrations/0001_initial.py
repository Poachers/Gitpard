# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('branch', models.CharField(max_length=50, verbose_name='\u0418\u043c\u044f \u0432\u0435\u0442\u043a\u0438')),
                ('datetime', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0438 \u043e\u0442\u0447\u0451\u0442\u0430')),
                ('mask', models.CharField(max_length=1000, verbose_name='\u041c\u0430\u0441\u043a\u0430')),
                ('kind', models.IntegerField(verbose_name='\u0422\u0438\u043f \u043e\u0442\u0447\u0451\u0442\u0430', choices=[(1, '\u041e\u0442\u0447\u0451\u0442 \u043f\u043e \u0430\u0432\u0442\u043e\u0440\u0430\u043c'), (2, '\u041e\u0442\u0447\u0451\u0442 \u043f\u043e \u0444\u0430\u0439\u043b\u0430\u043c')])),
                ('report', models.CharField(max_length=4000, verbose_name='\u041e\u0442\u0447\u0451\u0442', blank=True)),
                ('path', models.CharField(unique=True, max_length=140, verbose_name='\u041f\u0443\u0442\u044c \u0434\u043e \u043e\u0442\u0447\u0451\u0442\u0430 \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0435', blank=True)),
                ('repository', models.ForeignKey(to='repository.Repository')),
            ],
        ),
    ]
