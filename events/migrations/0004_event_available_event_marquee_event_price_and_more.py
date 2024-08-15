# Generated by Django 5.0.7 on 2024-08-04 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='event',
            name='marquee',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='event',
            name='timeline',
            field=models.CharField(choices=[('EV', 'Evening'), ('MT', 'Matinee'), ('NS', 'No Service')], default='EV', max_length=3),
        ),
    ]
