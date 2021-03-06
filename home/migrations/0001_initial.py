# Generated by Django 2.1.2 on 2018-10-16 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('char_id', models.CharField(db_index=True, max_length=8)),
                ('title', models.CharField(max_length=128)),
                ('expiration_datetime', models.DateTimeField(blank=True, null=True)),
                ('hits', models.IntegerField(db_index=True, default=0)),
                ('text', models.TextField(default='', max_length=100000)),
                ('deleted', models.BooleanField(default=False)),
                ('submitted', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
        ),
    ]
