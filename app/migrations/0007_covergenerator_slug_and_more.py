# Generated by Django 4.2 on 2024-03-25 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_homepage_alter_covergenerator_cover'),
    ]

    operations = [
        migrations.AddField(
            model_name='covergenerator',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='covergenerator',
            name='resized_cover',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
