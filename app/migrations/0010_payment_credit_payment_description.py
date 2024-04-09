# Generated by Django 4.2 on 2024-04-01 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_payment_plan_alter_covergenerator_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='credit',
            field=models.PositiveIntegerField(default=25),
        ),
        migrations.AddField(
            model_name='payment',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]