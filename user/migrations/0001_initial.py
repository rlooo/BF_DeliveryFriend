# Generated by Django 3.2.7 on 2022-07-09 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_login_id', models.IntegerField(unique=True)),
                ('email', models.EmailField(max_length=100, null=True)),
                ('nickname', models.CharField(max_length=20, unique=True)),
                ('profile_image', models.CharField(blank=True, default='https://png.pngtree.com/element_our/20200610/ourlarge/pngtree-character-default-avatar-image_2237203.jpg', max_length=2000, null=True)),
                ('longitude', models.CharField(blank=True, max_length=200, null=True)),
                ('latitude', models.CharField(blank=True, max_length=200, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
