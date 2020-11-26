# Generated by Django 3.0.9 on 2020-11-25 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('App', '0004_auto_20201126_0152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CommentsOwner', models.CharField(max_length=50)),
                ('CommentsOwnerId', models.IntegerField()),
                ('Comment', models.TextField()),
                ('PostId', models.IntegerField()),
                ('CommentTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PostId', models.IntegerField()),
                ('OwnerId', models.IntegerField()),
                ('LikeStatus', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NotificationOwner', models.CharField(max_length=20)),
                ('NotificationOwnerId', models.IntegerField()),
                ('NotificationType', models.CharField(max_length=20)),
                ('NotificationSentBy', models.CharField(max_length=20)),
                ('NotificationPostId', models.IntegerField()),
                ('NotificationTime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=50)),
                ('Content', models.TextField(max_length=200)),
                ('IsComment', models.BooleanField(default=0)),
                ('Time', models.DateTimeField(auto_now_add=True)),
                ('OwnerUsername', models.CharField(max_length=50)),
                ('OwnerId', models.IntegerField()),
                ('OwnerName', models.CharField(max_length=50)),
                ('OwnerSurname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SavePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SaveOwnerId', models.IntegerField()),
                ('SavePostId', models.IntegerField()),
                ('SaveStatus', models.BooleanField(default=False)),
            ],
        ),
    ]