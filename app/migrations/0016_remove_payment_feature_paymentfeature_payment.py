# Generated by Django 4.2 on 2024-04-15 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_faq_paymentfeature_payment_feature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='feature',
        ),
        migrations.AddField(
            model_name='paymentfeature',
            name='payment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payment_plan', to='app.payment'),
        ),
    ]