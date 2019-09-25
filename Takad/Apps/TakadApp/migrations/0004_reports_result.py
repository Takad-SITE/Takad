# Generated by Django 2.2.5 on 2019-09-25 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TakadApp', '0003_auto_20190923_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reports_result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_scan', models.TextField()),
                ('is_file', models.BooleanField(default=False)),
                ('dict_report', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_report', to='TakadApp.Users')),
            ],
        ),
    ]
