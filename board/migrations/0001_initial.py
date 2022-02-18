# Generated by Django 3.2.7 on 2022-02-18 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20)),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('text', models.TextField()),
                ('date', models.DateTimeField()),
                ('longitude', models.DecimalField(decimal_places=14, max_digits=17)),
                ('latitude', models.DecimalField(decimal_places=14, max_digits=16)),
                ('price', models.IntegerField()),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='%Y/%m/%d', verbose_name='썸네일')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.account')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='board.category')),
            ],
            options={
                'db_table': 'board',
            },
        ),
    ]
