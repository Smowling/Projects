# Generated by Django 4.1.2 on 2022-11-09 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_alter_bids_options_alter_auction_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bids',
            options={'get_latest_by': 'date'},
        ),
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auction_category', to='auctions.category'),
        ),
    ]
