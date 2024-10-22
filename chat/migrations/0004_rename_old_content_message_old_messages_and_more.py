# Generated by Django 5.1.1 on 2024-09-30 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_room_created'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='old_content',
            new_name='old_messages',
        ),
        migrations.RemoveField(
            model_name='message',
            name='receiver_location',
        ),
        migrations.RemoveField(
            model_name='message',
            name='sender_location',
        ),
        migrations.AlterField(
            model_name='message',
            name='message',
            field=models.TextField(blank=True, null=True, verbose_name='Message'),
        ),
    ]