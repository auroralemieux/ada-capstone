# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-05 02:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('babynamebook', '0004_auto_20170704_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='babynamebook.Name'),
        ),
    ]
