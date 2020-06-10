# Generated by Django 2.2.10 on 2020-06-07 06:54

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
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('college', models.CharField(max_length=50)),
                ('place', models.CharField(max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('name', models.CharField(max_length=20)),
                ('year', models.IntegerField()),
                ('subjects', models.CharField(max_length=150)),
                ('college_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.College')),
            ],
            options={
                'unique_together': {('college_n', 'name', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('empid', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('image', models.ImageField(null=True, upload_to='media/')),
                ('college_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.College')),
            ],
            options={
                'unique_together': {('college_n', 'empid')},
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True)),
                ('name', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('valid', models.BooleanField(default=False, editable=False)),
                ('college_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.College')),
                ('course_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.Course')),
            ],
            options={
                'unique_together': {('college_n', 'number')},
            },
        ),
        migrations.CreateModel(
            name='Ef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extra_feed', models.CharField(max_length=200, null=True)),
                ('college_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.College')),
                ('student_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.Student')),
            ],
        ),
        migrations.CreateModel(
            name='Teach',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=30)),
                ('college_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.College')),
                ('course_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.Course')),
                ('faculty_n', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='feedback.Faculty')),
            ],
            options={
                'unique_together': {('college_n', 'course_n', 'subject')},
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=40)),
                ('ct', models.IntegerField()),
                ('b', models.IntegerField()),
                ('ec', models.IntegerField()),
                ('t', models.IntegerField()),
                ('sc', models.IntegerField()),
                ('month', models.CharField(max_length=20)),
                ('year', models.CharField(max_length=4)),
                ('date', models.DateField(auto_now_add=True)),
                ('college_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.College')),
                ('faculty_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.Faculty')),
                ('student_n', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='feedback.Student')),
            ],
            options={
                'unique_together': {('college_n', 'student_n', 'faculty_n', 'subject', 'month', 'year')},
            },
        ),
    ]
