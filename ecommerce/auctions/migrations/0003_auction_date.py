# Generated by Django 4.1.2 on 2022-10-27 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_category_comments_bids_auction_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
