# Generated by Django 4.2.3 on 2023-07-07 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bandplannerapi', '0003_alter_banduser_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundlerelease',
            name='bundle_title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='gig',
            name='city_state',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='gig',
            name='venue',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='mediacontact',
            name='contact',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='mediacontact',
            name='organization',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='mediacontact',
            name='role',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='pressclipping',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='setlist',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='singlerelease',
            name='song_title',
            field=models.CharField(max_length=200),
        ),
    ]
