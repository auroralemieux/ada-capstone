# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-06 04:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babynamebook', '0007_person_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birth_year',
            field=models.IntegerField(),
        ),
    ]
