# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=140, verbose_name='\u0441\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u0439')),
                ('path', models.CharField(unique=True, max_length=140, verbose_name='\u041f\u0443\u0442\u044c \u0434\u043e \u043f\u0430\u043f\u043a\u0438 \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u044f \u043d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0435.')),
                ('login', models.CharField(max_length=140, verbose_name='\u041b\u043e\u0433\u0438\u043d \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u044f \u0434\u043b\u044f \u043f\u0440\u0438\u0432\u0430\u0442\u043d\u044b\u0445 \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u0435\u0432', blank=True)),
                ('password', models.CharField(max_length=50, verbose_name='\u041f\u0430\u0440\u043e\u043b\u044c \u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044f \u0434\u043b\u044f \u043f\u0440\u0438\u0432\u0430\u0442\u043d\u044b\u0445 \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u0435\u0432', blank=True)),
                ('name', models.CharField(max_length=140, verbose_name='\u0438\u043c\u044f \u043f\u0440\u043e\u0435\u043a\u0442\u0430', blank=True)),
                ('kind', models.IntegerField(verbose_name='\u0422\u0438\u043f \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u044f.', choices=[(0, b'public'), (1, b'private')])),
                ('state', models.IntegerField(default=0, verbose_name='\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435 \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u044f.', choices=[(0, '\u041d\u0435 \u0437\u0430\u0433\u0440\u0443\u0436\u0435\u043d'), (1, '\u0417\u0430\u0433\u0440\u0443\u0436\u0430\u0435\u0442\u0441\u044f'), (2, '\u0417\u0430\u0433\u0440\u0443\u0436\u0435\u043d'), (3, '\u041e\u0431\u043d\u043e\u0432\u043b\u044f\u0435\u0442\u0441\u044f'), (-1, '\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u0437\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c'), (-2, '\u041d\u0435 \u0443\u0434\u0430\u043b\u043e\u0441\u044c \u043e\u0431\u043d\u043e\u0432\u0438\u0442\u044c')])),
                ('last_modify', models.DateTimeField(verbose_name='\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0433\u043e \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='repository',
            unique_together=set([('url', 'user')]),
        ),
    ]
