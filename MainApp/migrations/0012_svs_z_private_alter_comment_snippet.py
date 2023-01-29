# Generated by Django 4.1.1 on 2023-01-17 10:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0011_alter_svs_k_name_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='svs_z',
            name='private',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='snippet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='MainApp.svs_z'),
        ),
    ]