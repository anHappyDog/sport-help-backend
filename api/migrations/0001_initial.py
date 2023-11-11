# Generated by Django 4.2.6 on 2023-11-11 16:26

import api.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('imageId', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='images/')),
                ('createTime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'Image',
            },
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('sportId', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sportName', models.CharField(max_length=32, unique=True)),
                ('sportDescription', models.CharField(max_length=256)),
                ('sportCoverName', models.CharField(default='defaultSportCover.jpg', max_length=64)),
            ],
            options={
                'db_table': 'Sport',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('teamId', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('teamName', models.CharField(default='kossur', max_length=128, unique=True)),
                ('maxPerson', models.IntegerField(default=8, validators=[api.models.validate_max_person_greater_than_2])),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('startTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('endTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('curPersonCnt', models.IntegerField(default=1, validators=[api.models.validate_cur_person_lte_max_person])),
                ('teamState', models.CharField(choices=[('R', 'RENEW'), ('O', 'ON'), ('E', 'END')], max_length=1, null=True)),
            ],
            options={
                'db_table': 'Team',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=64, unique=True)),
                ('password', models.CharField(default='', max_length=128)),
                ('email', models.EmailField(default='', max_length=256)),
                ('phone', models.CharField(default='', max_length=16)),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('avatar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.image')),
            ],
            options={
                'db_table': 'User',
            },
        ),
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
        migrations.AddField(
            model_name='team',
            name='createPerson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
        migrations.AddField(
            model_name='team',
            name='sportType',
            field=models.ForeignKey(default='其他运动', on_delete=django.db.models.deletion.CASCADE, to='api.sport', to_field='sportName'),
        ),
        migrations.CreateModel(
            name='SportRecord',
            fields=[
                ('sportRecordId', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('isTeam', models.BooleanField(default=False)),
                ('sportId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.sport')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
            options={
                'db_table': 'SportRecord',
            },
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('createTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('createUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
            options={
                'db_table': 'FeedBack',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('articleId', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(default='有趣的文章~', max_length=128)),
                ('content', models.TextField()),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
            options={
                'db_table': 'Article',
            },
        ),
    ]
