import django.db.models.deletion
import tracker.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_gospodarstwo_cel_gospodarstwo_przychod_gospodarstwo_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='gospodarstwo',
            name='kod',
            field=models.CharField(default=tracker.models.generuj_kod, max_length=10, unique=True),
        ),
        migrations.CreateModel(
            name='CzlonekGospodarstwa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rola', models.CharField(choices=[('admin', 'Administrator'), ('member', 'Członek')], default='member', max_length=10)),
                ('gospodarstwo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.gospodarstwo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'gospodarstwo')},
            },
        ),
        migrations.RemoveField(
            model_name='gospodarstwo',
            name='uzytkownicy',
        ),
        migrations.AddField(
            model_name='gospodarstwo',
            name='uzytkownicy',
            field=models.ManyToManyField(related_name='gospodarstwa', through='tracker.CzlonekGospodarstwa', to=settings.AUTH_USER_MODEL),
        ),
    ]