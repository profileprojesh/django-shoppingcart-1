# Generated by Django 3.1.1 on 2021-03-17 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='orderid',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]