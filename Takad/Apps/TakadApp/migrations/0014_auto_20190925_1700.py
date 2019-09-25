# Generated by Django 2.2.5 on 2019-09-25 14:00

import datetime
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TakadApp', '0013_auto_20190925_1700'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports_result2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_scan', models.TextField()),
                ('is_file', models.BooleanField(default=False)),
                ('dict_report', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2019, 9, 25, 17, 0, 49, 997639))),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TakadApp.Users')),
            ],
        ),
        migrations.DeleteModel(
            name='Reports_result',
        ),
    ]
