# Generated by Django 5.0.6 on 2024-07-31 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artisans', '0013_portfoliophoto_dateajout'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='Competence',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Competence',
            field=models.ManyToManyField(blank=True, to='artisans.tache'),
        ),
    ]
