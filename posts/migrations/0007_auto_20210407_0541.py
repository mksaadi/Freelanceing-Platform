# Generated by Django 3.0 on 2021-04-06 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_rating'),
        ('posts', '0006_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobappointment',
            name='receiver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_receiver', to='profiles.Profile'),
        ),
        migrations.AddField(
            model_name='jobappointment',
            name='sender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_sender', to='profiles.Profile'),
        ),
    ]
