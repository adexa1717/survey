# Generated by Django 3.2.6 on 2021-08-07 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_useranswerquestion_new_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswerquestion',
            name='new_answer',
            field=models.TextField(blank=True, null=True, verbose_name='текст своего ответа'),
        ),
    ]