# Generated by Django 4.0.8 on 2022-12-07 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_rename_name_en_us_category_name_en_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postCategory',
            field=models.ManyToManyField(through='news.PostCategory', to='news.category', verbose_name='category'),
        ),
    ]
