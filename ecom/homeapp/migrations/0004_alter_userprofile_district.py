# Generated by Django 4.1.7 on 2023-04-02 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeapp', '0003_alter_userprofile_district'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='district',
            field=models.CharField(blank=True, choices=[('Hydrabad', 'Hydrabad'), ('Kozhikkode', 'Kozhikkode'), ('Thiruvananthapuram', 'Thiruvananthapuram'), ('Hubli', 'Hubli'), ('Ernakulam', 'Ernakulam'), ('Banglore', 'Banglore'), ('Madurai', 'Madurai'), ('Coimbator', 'Coimbator'), ('Kannur', 'Kannur')], max_length=20, null=True),
        ),
    ]
