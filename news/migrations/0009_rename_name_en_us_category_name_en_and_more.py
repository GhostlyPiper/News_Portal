# Generated by Django 4.0.8 on 2022-12-05 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_rename_name_en_category_name_en_us_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='name_en_us',
            new_name='name_en',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='text_en_us',
            new_name='text_en',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='text_en_us',
            new_name='text_en',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='title_en_us',
            new_name='title_en',
        ),
    ]