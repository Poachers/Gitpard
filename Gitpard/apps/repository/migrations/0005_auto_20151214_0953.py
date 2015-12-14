# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repository', '0004_auto_20151130_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='RepoIssueLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(verbose_name='\u0422\u0438\u043f', choices=[(-1, '\u041e\u0448\u0438\u0431\u043a\u0430'), (1, '\u0423\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0435: \u0437\u0430\u0434\u0430\u0447\u0430 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0430'), (0, '\u0423\u0432\u0435\u0434\u043e\u043c\u043b\u0435\u043d\u0438\u0435: \u0437\u0430\u0434\u0430\u0447\u0430 \u043d\u0435 \u0432\u044b\u043f\u043e\u043b\u043d\u0435\u043d\u0430')])),
                ('module', models.IntegerField(verbose_name='\u041c\u043e\u0434\u0443\u043b\u044c', choices=[(0, '\u0412\u0441\u0435 \u043c\u043e\u0434\u0443\u043b\u0438'), (1, '\u041c\u043e\u0434\u0443\u043b\u044c \u0440\u0435\u043f\u043e\u0437\u0438\u0442\u043e\u0440\u0438\u0438'), (2, '\u041c\u043e\u0434\u0443\u043b\u044c \u0430\u043d\u0430\u043b\u0438\u0437'), (3, '\u041c\u043e\u0434\u0443\u043b\u044c \u043e\u0442\u0447\u0451\u0442\u044b')])),
                ('message', models.CharField(max_length=140, verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043e\u0448\u0438\u0431\u043a\u0438')),
                ('description', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043e\u0448\u0438\u0431\u043a\u0438')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'RepoIssueLogs',
            },
        ),
        migrations.AlterModelOptions(
            name='repository',
            options={'verbose_name_plural': 'Repositories'},
        ),
        migrations.AddField(
            model_name='repoissuelog',
            name='repo',
            field=models.ForeignKey(to='repository.Repository'),
        ),
        migrations.AddField(
            model_name='repoissuelog',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
