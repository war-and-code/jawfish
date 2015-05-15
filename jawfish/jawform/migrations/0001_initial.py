# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target', models.CharField(max_length=200)),
                ('addr', models.CharField(max_length=200)),
                ('vuln_var', models.CharField(max_length=200)),
                ('method', models.CharField(max_length=200)),
                ('goal_text', models.CharField(max_length=200)),
            ],
        ),
    ]
