# Generated by Django 5.2 on 2025-05-18 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0005_alter_producto_responsable_delete_responsable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='area',
        ),
        migrations.AddField(
            model_name='producto',
            name='aula',
            field=models.CharField(default='Aula General', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='edificio',
            field=models.CharField(default='General', max_length=100),
            preserve_default=False,
        ),
    ]
