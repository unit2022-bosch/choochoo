# Generated by Django 4.0.4 on 2022-04-13 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choochoo_app', '0002_alter_pathsegment_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
