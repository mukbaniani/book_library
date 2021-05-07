# Generated by Django 3.2 on 2021-04-22 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='წიგნის სახელი')),
                ('author', models.CharField(max_length=100, verbose_name='ავტორი')),
                ('quantity', models.IntegerField(default=0, verbose_name='მარაგი')),
                ('Condition', models.IntegerField(default=10, verbose_name='წიგნის მდოგმარეობა')),
            ],
            options={
                'verbose_name': 'წიგნები',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100, verbose_name='მისამართი')),
                ('work_day', models.CharField(max_length=40, verbose_name='სამუშაო დღეები')),
                ('tel_number', models.CharField(max_length=40, verbose_name='ტელეფონის ნომერი')),
            ],
            options={
                'verbose_name': 'ფილიალები',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(verbose_name='შეკვეთის დრო')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='დაბრუნების დრო')),
                ('status', models.BooleanField(default=False, verbose_name='სტატუსი')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book', verbose_name='წიგნი')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.branch', verbose_name='ფილიალი')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='მომხმარებელი')),
            ],
            options={
                'verbose_name': 'შეკვეთები',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('return_time', models.BooleanField(verbose_name='დააბრუნა მის დროზე?')),
                ('condition', models.IntegerField(default=10, verbose_name='წიგნის მდოგმარეობა')),
                ('return_book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.book', verbose_name='რომელი წიგნი დააბრუნა')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='მომხმარებელი')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='branch',
            field=models.ManyToManyField(to='library.Branch', verbose_name='ფილიალი'),
        ),
    ]
