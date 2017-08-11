# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-11 08:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.CharField(help_text='The price of the article', max_length=10)),
                ('largeText', models.CharField(help_text='The markdown text of the article', max_length=15000)),
                ('type', models.SmallIntegerField(help_text='The type of article (e.g. for example a t-shirt')),
                ('description', models.CharField(help_text='A short description of the article (e.g. heading)', max_length=100)),
                ('visible', models.BooleanField(help_text='Should the article be visible to the public yet?')),
                ('quantity', models.IntegerField(help_text='How many articles of this kind are left?')),
                ('size', models.CharField(help_text='The size of the article', max_length=10)),
                ('cachedText', models.CharField(help_text='The compiled markdown long text', max_length=15000)),
            ],
        ),
        migrations.CreateModel(
            name='ArticleMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Article')),
            ],
        ),
        migrations.CreateModel(
            name='ArticleRequested',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField()),
                ('notes', models.CharField(max_length=15000)),
                ('AID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Article')),
            ],
        ),
        migrations.CreateModel(
            name='GroupReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('ready', models.BooleanField()),
                ('open', models.BooleanField()),
                ('notes', models.CharField(max_length=15000)),
                ('pickupDate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(help_text='The category of the media', max_length=25)),
                ('headline', models.CharField(help_text='The heading of the image', max_length=50)),
                ('text', models.CharField(help_text='A longer text matching the image', max_length=15000)),
                ('cachedText', models.CharField(help_text='The compiled version of the markdown >text<', max_length=15000)),
                ('lowResFile', models.CharField(help_text='A link to a low resolution version of the image', max_length=15000)),
                ('highResFile', models.CharField(help_text='A link to a high resolution version of the image', max_length=15000)),
                ('uploadTimestamp', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MediaUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Media')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('cacheText', models.CharField(help_text='The compiled version of the markdown >text<', max_length=15000)),
                ('visibleLevel', models.SmallIntegerField(help_text='What access level does the viewer need to have a look at this')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(help_text='The markdown version of the article text', max_length=15000)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creationTimestamp', models.DateTimeField(auto_now=True)),
                ('notes', models.CharField(help_text='some notes on the user (for example additional contact channels)', max_length=15000)),
                ('active', models.BooleanField()),
                ('dect', models.IntegerField()),
                ('rights', models.SmallIntegerField()),
                ('displayName', models.CharField(max_length=75)),
                ('authuser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('avatarMedia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontpage.Media')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('SName', models.CharField(editable=False, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('property', models.CharField(max_length=15000)),
                ('requiredLevel', models.SmallIntegerField()),
                ('changeTimestamp', models.DateTimeField(auto_now=True)),
                ('changeReason', models.CharField(max_length=15000)),
                ('changedByUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='createdByUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Profile'),
        ),
        migrations.AddField(
            model_name='mediaupload',
            name='UID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Profile'),
        ),
        migrations.AddField(
            model_name='groupreservation',
            name='createdByUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Profile'),
        ),
        migrations.AddField(
            model_name='articlerequested',
            name='RID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.GroupReservation'),
        ),
        migrations.AddField(
            model_name='articlemedia',
            name='MID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Media'),
        ),
        migrations.AddField(
            model_name='article',
            name='addedByUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='frontpage.Profile'),
        ),
        migrations.AddField(
            model_name='article',
            name='flashImage',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='frontpage.Media'),
        ),
    ]
