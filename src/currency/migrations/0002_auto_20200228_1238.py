# Generated by Django 2.2.10 on 2020-02-28 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rate',
            name='source',
            field=models.PositiveSmallIntegerField(choices=[(1, 'PrivatBank'), (2, 'MonoBank'), (3, 'OTPBank'), (4, 'vkurse.dp.ua'), (5, 'obmen.dp.ua'), (6, 'finance.i.ua')]),
        ),
    ]
