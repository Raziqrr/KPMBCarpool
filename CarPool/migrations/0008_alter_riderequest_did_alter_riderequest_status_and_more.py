# Generated by Django 4.2 on 2023-06-22 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CarPool', '0007_alter_driver_did_alter_routes_rid_alter_vehicle_vid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riderequest',
            name='dID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CarPool.driver'),
        ),
        migrations.AlterField(
            model_name='riderequest',
            name='status',
            field=models.CharField(default='Request Pending', max_length=128),
        ),
        migrations.AlterField(
            model_name='riderequest',
            name='vID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='CarPool.vehicle'),
        ),
    ]
