# Generated by Django 5.0.1 on 2024-03-09 02:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partsdatabase', '0020_alter_kithardwarekit_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kithardwareassembly',
            name='quantity',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
