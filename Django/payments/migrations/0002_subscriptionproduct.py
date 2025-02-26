# Generated by Django 3.2 on 2021-08-06 02:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionProduct',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.product')),
                ('subscription_duration', models.IntegerField(default=0)),
            ],
            bases=('payments.product',),
        ),
    ]
