# Generated by Django 4.0.6 on 2022-07-28 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dino', '0005_remove_question_right_answer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choices',
            name='true',
            field=models.BooleanField(default=False),
        ),
    ]
