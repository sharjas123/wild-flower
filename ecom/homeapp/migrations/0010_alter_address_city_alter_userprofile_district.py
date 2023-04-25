# Generated by Django 4.1.7 on 2023-04-04 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0009_alter_address_city_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Ernakulam', 'Ernakulam'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Kannur', 'Kannur')], max_length=255),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Coimbator', 'Coimbator'), ('Kozhikkode', 'Kozhikkode'), ('Hydrabad', 'Hydrabad'), ('Hubli', 'Hubli'), ('Ernakulam', 'Ernakulam'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Madurai', 'Madurai'), ('Banglore', 'Banglore'), ('Kannur', 'Kannur')], max_length=20, null=True),
        ),
    ]