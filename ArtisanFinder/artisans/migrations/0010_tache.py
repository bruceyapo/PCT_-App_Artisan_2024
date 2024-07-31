# Generated by Django 5.0.6 on 2024-07-30 20:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artisans', '0009_alter_userprofile_annee_experience'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tache',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('metier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taches', to='artisans.metier')),
            ],
        ),
    ]
