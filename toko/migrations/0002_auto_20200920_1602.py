# Generated by Django 3.1 on 2020-09-20 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toko', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produk',
            name='digital',
        ),
        migrations.AddField(
            model_name='produk',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
