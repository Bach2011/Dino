# Generated by Django 3.2.7 on 2022-07-17 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Dino', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rightanswer',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Dino.textanswer'),
        ),
    ]