# Generated by Django 5.1.2 on 2024-12-03 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PersonaleinsatzplanHaeH', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auftrag',
            name='massnahmenummer',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='auftrag',
            name='optionsnummer',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='auftrag',
            name='vergabenummer',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
