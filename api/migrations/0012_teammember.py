# Generated by Django 4.2.6 on 2023-11-09 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_team_teamname'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.team')),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
            options={
                'db_table': 'TeamMember',
            },
        ),
    ]