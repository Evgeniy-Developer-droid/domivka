# Generated by Django 4.0.4 on 2022-05-18 15:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0012_report_alter_realestate_service_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='realestateimage',
            name='real_estate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='public.realestate'),
        ),
    ]
