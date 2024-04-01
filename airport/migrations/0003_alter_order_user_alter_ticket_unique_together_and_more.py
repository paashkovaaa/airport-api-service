# Generated by Django 5.0.3 on 2024-03-26 11:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airport', '0002_crew_alter_ticket_options_airplane_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('flight', 'row', 'seat')},
        ),
        migrations.AddField(
            model_name='flight',
            name='crews',
            field=models.ManyToManyField(related_name='flights', to='airport.crew'),
        ),
    ]