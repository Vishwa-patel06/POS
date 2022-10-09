# Generated by Django 4.1 on 2022-09-02 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Static_Master', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
                ('gstNumber', models.CharField(blank=True, max_length=255, null=True)),
                ('contactNumber', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('contactEmail', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('customerWebsite', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('pincode', models.CharField(blank=True, max_length=255, null=True)),
                ('town', models.CharField(blank=True, max_length=255, null=True)),
                ('district', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, blank=True, chained_field='state', chained_model_field='stateObject', null=True, on_delete=django.db.models.deletion.CASCADE, to='Static_Master.districtmodel')),
                ('state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Static_Master.statemodel')),
                ('userObject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '    Customer List',
                'verbose_name_plural': '    Customer List',
            },
        ),
        migrations.CreateModel(
            name='CustomerBankModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountNumber', models.CharField(max_length=255)),
                ('ifsc', models.CharField(max_length=255)),
                ('BankObject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Static_Master.bankmodel')),
                ('customerObject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.customermodel')),
            ],
            options={
                'verbose_name': '  Bank List',
                'verbose_name_plural': '  Bank List',
            },
        ),
    ]