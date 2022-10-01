# Generated by Django 4.0.3 on 2022-04-11 10:43

import Expertize.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CEdocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fayl', models.FileField(blank=True, max_length=500, upload_to=Expertize.models.disch_doc_path, verbose_name='Загружаемый документ')),
            ],
            options={
                'verbose_name': 'Документ экспертизы',
                'verbose_name_plural': 'Документы экспертизы',
            },
        ),
        migrations.CreateModel(
            name='Cexpertiza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kolichestvo_istochnikov', models.IntegerField(blank=True, max_length=200, null=True, verbose_name='Количество источников')),
                ('neorganizovan_istochniki', models.CharField(blank=True, max_length=200, null=True, verbose_name='Количество неорганизованных источников')),
                ('data', models.DateField(blank=True, null=True, verbose_name='Дата начала экспертизы')),
                ('nomer_expertizi', models.CharField(blank=True, max_length=100, verbose_name='Номер экспертизы')),
                ('is_deleted', models.BooleanField(blank=True, default=False, verbose_name='Передана в архив')),
            ],
            options={
                'verbose_name': 'Экспертиза организации',
                'verbose_name_plural': 'Экспертизы организации',
                'ordering': ('nomer_expertizi',),
            },
        ),
        migrations.CreateModel(
            name='DannieCheloveka',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imya', models.CharField(max_length=200, verbose_name='Имя человека')),
                ('familiya', models.CharField(max_length=200, verbose_name='Фамилия человека')),
                ('otchestvo', models.CharField(max_length=200, verbose_name='Отчество человека')),
                ('pochta', models.CharField(max_length=200, verbose_name='Почта человека')),
            ],
            options={
                'verbose_name': 'Данные человека',
                'verbose_name_plural': 'Данные людей',
                'ordering': ('familiya',),
            },
        ),
        migrations.CreateModel(
            name='DDmtu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('krat', models.CharField(max_length=50, verbose_name='Краткое название МТУ')),
                ('poln', models.CharField(blank=True, max_length=500, verbose_name='Полное название МТУ')),
            ],
            options={
                'verbose_name': 'МТУ',
                'verbose_name_plural': 'МТУ',
                'ordering': ('krat',),
            },
        ),
        migrations.CreateModel(
            name='DEtipExperizi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.CharField(max_length=200, verbose_name='Тип государственной услуги (выброс / сброс)')),
                ('opisanie', models.TextField(verbose_name='Описание типа Экспертизы')),
            ],
            options={
                'verbose_name': 'Тип экспертизы',
                'verbose_name_plural': 'Типы экспертизы',
            },
        ),
        migrations.CreateModel(
            name='DOtipObyect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.CharField(max_length=200, verbose_name='Тип объекта')),
            ],
            options={
                'verbose_name': 'Тип объекта',
                'verbose_name_plural': 'Типы объекта',
                'ordering': ('tip',),
            },
        ),
        migrations.CreateModel(
            name='DProli',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rol', models.CharField(max_length=200, verbose_name='Роль человека')),
            ],
            options={
                'verbose_name': 'Роль человека',
                'verbose_name_plural': 'Роли человека',
                'ordering': ('rol',),
            },
        ),
        migrations.CreateModel(
            name='Dtip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.TextField(verbose_name='Тип документа')),
            ],
            options={
                'verbose_name': 'Тип',
                'verbose_name_plural': 'Типы',
                'ordering': ('tip',),
            },
        ),
        migrations.CreateModel(
            name='DTipData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opisanie', models.TextField(verbose_name='Описание даты')),
            ],
            options={
                'verbose_name': 'Тип даты',
                'verbose_name_plural': 'Типы даты',
                'ordering': ('opisanie',),
            },
        ),
        migrations.CreateModel(
            name='DtipDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.cedocument', verbose_name='Выбор необходимого документа')),
                ('tip', models.ForeignKey(blank=True, max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.dtip', verbose_name='Выбор необходимого типа документа')),
            ],
            options={
                'verbose_name': 'Тип документа',
                'verbose_name_plural': 'Типы документа',
            },
        ),
        migrations.CreateModel(
            name='JERPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertiza', models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.cexpertiza', verbose_name='Выбор необходимой экспертизы')),
                ('person', models.ForeignKey(blank=True, max_length=2000, on_delete=django.db.models.deletion.CASCADE, to='Expertize.danniecheloveka', verbose_name='Выбор необходимого человека')),
                ('rol', models.ForeignKey(blank=True, max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.dproli', verbose_name='Выбор необходимой роли')),
            ],
            options={
                'verbose_name': 'Участник экспертизы',
                'verbose_name_plural': 'Участники экспертизы',
            },
        ),
        migrations.CreateModel(
            name='JDDrazr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomer', models.CharField(blank=True, max_length=100, verbose_name='Номер разрешения')),
                ('opisanie', models.TextField(blank=True, verbose_name='Дополнительные сведения')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Expertize.dtipdocument', verbose_name='Тип документа')),
                ('kem_vidano', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Expertize.ddmtu', verbose_name='Кем выдано')),
            ],
            options={
                'verbose_name': 'Разрешение',
                'verbose_name_plural': 'Разрешения',
            },
        ),
        migrations.CreateModel(
            name='JdataDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(blank=True, verbose_name='Дата выдачи / получения документа')),
                ('document', models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.cedocument', verbose_name='Выбор необходимого документа')),
                ('opisanie_data', models.ForeignKey(blank=True, max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.dtipdata', verbose_name='Тип даты')),
            ],
            options={
                'verbose_name': 'Дата документов',
                'verbose_name_plural': 'Даты документов',
            },
        ),
        migrations.CreateModel(
            name='Corganizaciya',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazvanie_korotkoe', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название объекта короткое')),
                ('nazvanie_polnoe', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название объекта полное')),
                ('nazvanie_select', models.CharField(blank=True, max_length=200, null=True, verbose_name='Название для Select')),
                ('opisanie', models.TextField(verbose_name='Описание объекта')),
                ('tip', models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.dotipobyect', verbose_name='Тип объекта')),
            ],
            options={
                'verbose_name': 'Название организации',
                'verbose_name_plural': 'Названия организации',
                'ordering': ('nazvanie_korotkoe',),
            },
        ),
        migrations.AddField(
            model_name='cexpertiza',
            name='organizaciya',
            field=models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.corganizaciya', verbose_name='Название объекта'),
        ),
        migrations.AddField(
            model_name='cexpertiza',
            name='tip',
            field=models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.detipexperizi', verbose_name='Тип экспертизы'),
        ),
        migrations.AddField(
            model_name='cedocument',
            name='expertiza',
            field=models.ForeignKey(max_length=200, on_delete=django.db.models.deletion.CASCADE, to='Expertize.cexpertiza', verbose_name='Выбор необходимой экспертизы'),
        ),
    ]
