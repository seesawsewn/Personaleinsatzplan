# Generated by Django 5.1.2 on 2024-11-27 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PersonaleinsatzplanHaeH', '0002_mitarbeiterbetreuungsschluessel_eingesetzte_stunden_im_plan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mitarbeiterbetreuungsschluessel',
            name='eingesetzte_stunden_im_plan',
        ),
        migrations.RemoveField(
            model_name='mitarbeiterbetreuungsschluessel',
            name='freie_stunden_im_plan',
        ),
        migrations.AddField(
            model_name='mitarbeiterbetreuungsschluessel',
            name='freie_stunden',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='mitarbeiterbetreuungsschluessel',
            name='zugewiesene_stunden',
            field=models.FloatField(default=0),
        ),
    ]