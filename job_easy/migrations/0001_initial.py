# Generated by Django 2.2 on 2019-12-13 08:50

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_employer', models.BooleanField(default=False)),
                ('is_employee', models.BooleanField(default=False)),
                ('is_data_seeker', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='aadhaar_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('yob', models.CharField(max_length=10)),
                ('co', models.CharField(max_length=150)),
                ('house', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('loc', models.CharField(max_length=50)),
                ('vtc', models.CharField(max_length=50)),
                ('dist', models.CharField(max_length=50)),
                ('subdist', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('pc', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('resume_bool', models.BooleanField(default=False)),
                ('resume_file_new', models.FileField(upload_to='')),
                ('details_and_instructions', models.TextField(blank=True)),
                ('application_status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('last_date', models.DateTimeField(blank=True)),
                ('job_title', models.TextField(null=True)),
                ('job_type', models.CharField(max_length=150)),
                ('job_details_requirements', models.TextField(blank=True)),
                ('job_address', models.TextField(null=True)),
                ('job_salary', models.CharField(blank=True, max_length=50)),
                ('job_other_details', models.TextField(blank=True)),
                ('job_terms_and_conditions', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='third_party_job_applicants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_profile_picture', models.ImageField(blank=True, upload_to='user_profile_pictures')),
                ('company_name', models.CharField(max_length=50)),
                ('company_description', models.TextField()),
                ('company_adress', models.TextField()),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tpj_user', to='job_easy.job')),
            ],
        ),
        migrations.CreateModel(
            name='third_party_application_applicants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_profile_picture', models.ImageField(blank=True, upload_to='user_profile_pictures')),
                ('phone_no', models.CharField(max_length=50)),
                ('address', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tpa_user', to='job_easy.job')),
            ],
        ),
        migrations.CreateModel(
            name='savedjobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='job_easy.job')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='employer_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=50)),
                ('address', models.TextField(null=True)),
                ('user_profile_pictures', models.ImageField(blank=True, upload_to='user_profile_pictures')),
                ('company_name', models.CharField(max_length=50)),
                ('company_type', models.CharField(max_length=50)),
                ('company_description', models.TextField(null=True)),
                ('company_adress', models.TextField(null=True)),
                ('verification_status', models.BooleanField(default=False)),
                ('privacy_status', models.BooleanField(default=False)),
                ('aadhaar_details', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aadhaar_details_employer', to='job_easy.aadhaar_info')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='employee_profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_no', models.CharField(max_length=50)),
                ('address', models.TextField(null=True)),
                ('user_profile_pictures', models.ImageField(blank=True, upload_to='user_profile_pictures')),
                ('verification_status', models.BooleanField(default=False)),
                ('privacy_status', models.BooleanField(default=False)),
                ('job_status', models.BooleanField(default=False)),
                ('aadhaar_details', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aadhaar_details_employee', to='job_easy.aadhaar_info')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='credibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ratings', models.TextField(null=True)),
                ('comments', models.TextField(null=True)),
                ('on_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='job_easy.application')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credibility_of_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='application',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_application', to='job_easy.job'),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aplication_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
