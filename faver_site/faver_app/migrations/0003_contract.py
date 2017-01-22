# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-21 20:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faver_app', '0002_faverrequest_issuer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acceptor', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='acceptor', to='faver_app.FaverUser')),
                ('issuer', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='issuer', to='faver_app.FaverUser')),
                ('request', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, related_name='request', to='faver_app.FaverRequest')),
            ],
        ),
    ]